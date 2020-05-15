from time import time

from util import gen_id, read_json, write_json
from wrap import *


class database():
    def __init__(self, file):
        self.file = file
        self.db = read_json(file)

    def save(self):
        write_json(self.file, self.db)

    def get_keys(self):
        return list(self.db.keys())

    def has_key(self, key):
        return key in self.get_keys()

    @auto_save
    def gen_key(self, max=10):
        key = gen_id()
        self.db[key] = {'uid': {}, 'max': max}
        return key

    @auto_save
    def del_key(self, key):
        self.db.pop(key)

    @validate_key([])
    def get_uids(self, key):
        return list(self.db[key]['uid'].keys())

    @validate_key(False)
    def has_uid(self, key, uid):
        return uid in self.get_uids(key)

    @validate_key(False)
    @auto_save
    def update_uid(self, key, uid):
        self.db[key]['uid'][uid] = time()
        return True

    @validate_key(None)
    @auto_save
    def del_uid(self, key, uid):
        self.db[key]['uid'].pop(uid)

    def last_seen(self, key, uid):
        return self.db[key]['uid'][uid] \
            if self.has_uid(key, uid) \
            else 0

    @validate_key(0)
    def get_max(self, key):
        return self.db[key]['max']

    def full(self, key):
        return len(self.get_uids(key)) >= self.get_max(key)

    def get_inactive(self, key, time_out=90):
        if len(self.get_uids(key)) < 1:
            return ''
        sort = {
            k: v for k, v in sorted(
                self.db[key]['uid'].items(),
                key=lambda item: item[1]
            )
        }
        return sort.keys()[0] \
            if sort.values()[0] + time_out <= time() \
            else ''

    def reclain(self, time_out=90):
        for key in self.get_keys():
            while True:
                uid = self.get_inactive(key, time_out)
                if not uid:
                    break
                self.del_uid(key, uid)
