from util import write_json, read_json, gen_id
from time import time


def save_on_change(func):
    def wrapper(self, *args, **kw):
        ret = func(self, *args, **kw)
        self.save()
        return ret
    return wrapper


class database():
    def __init__(self, filename):
        self.file = filename
        self.key = read_json(filename)

    def save(self):
        write_json(self.file, self.key)

    def get_keys(self):
        return self.key.keys()

    def has_key(self, key):
        return key in self.get_keys()

    @save_on_change
    def gen_key(self, max=10):
        key = gen_id()
        self.key[key] = {'uid': {}, 'max': max}
        return key

    @save_on_change
    def del_key(self, key):
        self.key.pop(key)

    def get_uids(self, key):
        if not self.has_key(key):
            return None
        return self.key[key]['uid'].get_keys()

    def has_uid(self, key, uid):
        return uid in self.get_uids(key)

    @save_on_change
    def add_uid(self, key, uid):
        if key not in self.get_keys():
            return False
        self.key[key]['uid'][uid] = time()
        return True

    @save_on_change
    def update_uid(self, key, uid):
        if not self.has_uid(key, uid):
            return False
        self.key[key]['uid'][uid] = time()
        return True

    @save_on_change
    def del_uid(self, key, uid):
        if key not in self.get_keys():
            return
        self.key[key]['uid'].pop(uid)

    def get_max(self, key):
        if not self.has_key(key):
            return None
        return self.key[key]['max']

    def full(self, key):
        if not self.has_key(key):
            return False
        return len(self.get_uids(key)) <= self.get_max(key)

    def sort(self, key):
        if not self.has_key(key):
            return
        self.key[key]['uid'] = {
            k: v for k, v in sorted(
                self.key[key]['uid'].items(),
                key=lambda item: item[1]
            )
        }

    @save_on_change
    def squeeze(self, key, time_out=600):
        if not self.has_key(key):
            return False
        elif len(self.get_uids(key)) < 1:
            return False
        elif self.key[key]['uid'].values()[0] + time_out >= time():
            return False
        else:
            self.del_uid(key, self.key[key]['uid'].keys()[0])
            return True

    def reclain(self, key, time_out=600):
        while self.squeeze(key, time_out):
            pass

    def reclain_all(self, time_out=600):
        for key in self.key.keys():
            self.reclain(key, time_out)
