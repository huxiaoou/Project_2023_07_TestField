class CBase(object):
    def __init__(self, a: int, b: int, c: int):
        self.a, self.b, self.c = a, b, c

    def print(self):
        print(self.a, self.b, self.c)


class CA1(CBase):
    def __init__(self, d: int, b: int, **kwargs):
        super().__init__(b=b, **kwargs)
        self.d = d + b


class CA2(CA1):
    def __init__(self, e: int, **kwargs):
        super().__init__(**kwargs)
        self.e = e

    def print(self):
        super().print()
        print(f"d={self.d},e={self.e}")


shared_args = dict(a=1, b=2, c=3)
x = CA2(d=4, e=5, **shared_args)
x.print()
