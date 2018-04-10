"""Null Object pattern
"""
import random


class RealObject(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        return print("Called with args {} and kwargs {}".format(args, kwargs))

    def is_null(self):
        return False

    def do_stuff(self):
        print("do some real stuff")

    def get_stuff(self):
        return "some real stuff"


class NullObject(RealObject):

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return "<Null>"

    def __str__(self):
        return "Null"

    def __getattr__(self, attr_name):
        return self

    def __setattr__(self, attr_name, attr_value):
        return self

    def __delattr__(self, attr_name):
        return self

    def is_null(self):
        return True

    def do_stuff(self):
        pass

    def get_stuff(self):
        return None


def give_me_an_object(name):
    num = random.random()
    cls = RealObject if num > 0.5 else NullObject
    print("Class: {}".format(cls.__name__))
    print("__init__")
    return cls(name)


def main():
    name = "Bob"

    # instatiation and representation
    obj = give_me_an_object(name)
    print("__str__")
    print(obj)
    print(repr(obj))

    # attribute handling
    print("__getattr__ ")
    print(obj.name)
    print("__setattr__")
    obj.name = "John"
    print(obj.name)
    print("__delattr__")
    del obj.name

    # object calling
    print("__call__")
    obj("hello", 123, some_key=456)

    # methods for this particular example
    print("do_stuff")
    obj.do_stuff()
    my_stuff = obj.get_stuff()
    print(my_stuff)


if __name__ == "__main__":
    main()
