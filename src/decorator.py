def validate_key(ret):
    def decorator(func):
        def wrapper(self, *args, **kw):
            return func(self, *args, **kw) \
                if self.has_uid(args[0], args[1])\
                else ret
        return wrapper
    return decorator


def validate_uid(ret):
    def decorator(func):
        def wrapper(self, *args, **kw):
            return func(self, *args, **kw) \
                if self.has_key(args[0])\
                else ret
        return wrapper
    return decorator


def auto_save(func):
    def wrapper(self, *args, **kw):
        ret = func(self, *args, **kw)
        self.save()
        return ret
    return wrapper
