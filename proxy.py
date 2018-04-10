"""Proxy pattern

Proxy is a structural design pattern. A proxy is a surrogate object which can
communicate with the real object (aka implementation). Whenever a method in the
surrogate is called, the surrogate simply calls the corresponding method in
the implementation. The real object is encapsulated in the surrogate object when
the latter is instantiated. It's NOT mandatory that the real object class and
the surrogate object class share the same common interface.
"""
from abc import ABC, abstractmethod


class CommonInterface(ABC):
    """Common interface for Implementation (real obj) and Proxy (surrogate)."""

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def do_stuff(self):
        pass


class Implementation(CommonInterface):

    def __init__(self, filename):
        self.filename = filename

    def load(self):
        print("load {}".format(self.filename))

    def do_stuff(self):
        print("do stuff on {}".format(self.filename))


class Proxy(CommonInterface):

    def __init__(self, implementation):
        self.__implementation = implementation  # the real object
        self.__cached = False

    def load(self):
        self.__implementation.load()
        self.__cached = True

    def do_stuff(self):
        if not self.__cached:
            self.load()
        self.__implementation.do_stuff()


def main():
    p1 = Proxy(Implementation("RealObject1"))
    p2 = Proxy(Implementation("RealObject2"))

    p1.do_stuff()  # loading necessary
    p1.do_stuff()  # loading unnecessary (use cached object)
    p2.do_stuff()  # loading necessary
    p2.do_stuff()  # loading unnecessary (use cached object)
    p1.do_stuff()  # loading unnecessary (use cached object)


if __name__ == "__main__":
    main()
