class A(object):
    def __init__(self, a: int):
        self.a = a

    def printA(self):
        print(f"... this is class A, a = {self.a}")
        return 0


class B(object):
    def __init__(self, b: int):
        self.b = b

    def printB(self):
        print(f"... this is class B, b = {self.b}")
        return 0


class C(A, B):
    def __init__(self, a: int, b: int):
        super().__init__(a)


c = C(3, 4)
c.printA()
c.printB()
