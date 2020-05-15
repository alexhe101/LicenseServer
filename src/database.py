from util import write_json, read_json, gen_id
from time import time
from decorator import *


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

    @validate_key(None)
    def get_uids(self, key):
        return list(self.db[key]['uid'].keys())

    @validate_key(False)
    def has_uid(self, key, uid):
        return uid in self.get_uids(key)

    @validate_key(False)
    @auto_save
    def add_uid(self, key, uid):
        self.db[key]['uid'][uid] = time()
        return True

    @validate_uid(False)
    @auto_save
    def update_uid(self, key, uid):
        self.db[key]['uid'][uid] = time()
        return True

    @validate_uid(None)
    @auto_save
    def del_uid(self, key, uid):
        self.db[key]['uid'].pop(uid)

    @validate_uid(0)
    def last_seen(self, key, uid):
        return self.db[key]['uid'][uid]

    @validate_key(-1)
    def get_max(self, key):
        return self.db[key]['max']

    @validate_key(False)
    def full(self, key):
        return len(self.get_uids(key)) >= self.get_max(key)

    @validate_key(None)
    def sort(self, key):
        self.db[key]['uid'] = {
            k: v for k, v in sorted(
                self.db[key]['uid'].items(),
                key=lambda item: item[1]
            )
        }

    @validate_key(False)
    @auto_save
    def squeeze(self, key, time_out=600):
        if len(self.get_uids(key)) < 1:
            return False
        elif list(self.db[key]['uid'].values())[0] + time_out >= time():
            return False
        else:
            self.del_uid(key, self.get_uids(key)[0])
            return True

    def reclain(self, key, time_out=600):
        while self.squeeze(key, time_out):
            pass

    def reclain_all(self, time_out=600):
        for key in self.get_keys():
            self.reclain(key, time_out)
