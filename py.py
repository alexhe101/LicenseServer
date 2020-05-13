class c():
    def s(self):
        print('s called')

    def l(self, f):
        def wrapper(*args, **kw):
            f(self, *args, **kw)
            self.s()
        return wrapper

    @l
    def a(self, x):
        print(x)


n = c()
n.a(123456)
