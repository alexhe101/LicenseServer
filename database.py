from util import write_json, read_json, gen_id
from time import time


class database():
    def __init__(self, filename):
        self.file = filename
        self.key = read_json(filename)

    def save(self):
        write_json(self.file, self.key)

    def save_on_change(self, func):
        def wrapper(*args, **kw):
            func()
            self.save()
        return wrapper

    def get_keys(self):
        return self.key.keys()

    def has_key(self, key):
        return key in self.get_keys()

    @save_on_change
    def gen_key(self, max=10):
        key = gen_id()
        self.key[key] = {'uid': [], 'max': max}
        self.save()
        return key

    def del_key(self, key):
        self.key.pop(key)
        self.save()

    def get_uids(self, key):
        if not self.has_key(key):
            return None
        return self.key[key]['uid'].get_keys()

    def has_uid(self, key, uid):
        return uid in self.get_uids(key)

    def add_uid(self, key, uid):
        if key not in self.get_keys():
            return False
        self.key[key]['uid'][uid] = time()
        self.save()
        return True

    def update_uid(self, key, uid):
        if not self.has_uid(key, uid):
            return False
        self.key[key]['uid'][uid] = time()
        self.save()
        return True

    def del_uid(self, key, uid):
        self.key[key]['uid'].pop(uid)
        self.save()

    def get_max(self, key):
        if not self.has_key(key):
            return None
        return self.key[key]['max']
