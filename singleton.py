class Singleton(object):

    _instance = None

    def __init__(self, name):
        self.name = name

    def __new__(cls, *args):
        if getattr(cls, "_instance") is None or cls != cls._instance.__class__:
            cls._instance = object.__new__(cls)
        return cls._instance


class Child(Singleton):

    def childmethod(self):
        pass


class GrandChild(Child):

    def grandchildmethod(self):
        pass


def main():
    # The __new__ method creates a new instance and returns it.
    # The __init__ method initializes the instance.
    s1 = Singleton("Sam")
    # The __new__ method does NOT create an instance and returns the first one.
    # The __init__ method re-initializes the instance (the first one).
    # The instance is the same, so the effects of the first __init__ are lost.
    s2 = Singleton("Tom")
    # The __new__ method creates a new instance because it's a different class.
    c1 = Child("John")
    c2 = Child("Andy")
    g1 = GrandChild("Bob")
    print(s1.name, id(s1), s1)
    print(s2.name, id(s2), s2)
    print(c1.name, id(c1), c1)
    print(c2.name, id(c2), c2)
    print(g1.name, id(g1), g1)
    print("s1 is s2?")
    print(s1 is s2)
    print("s1 is c1?")
    print(s1 is c1)
    print("c1 is c2?")
    print(c1 is c2)
    print("c1 is g1?")
    print(c1 is g1)


if __name__ == "__main__":
    main()
