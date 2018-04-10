"""Singleton Pool

This is not an Object Pool, but a Singleton... but it's a funny example
"""
import atexit
import pprint


class PoolFull(Exception):
    pass


class PoolMeta(type):

    pool = dict()

    @staticmethod
    def serialize_arguments(cls, *args, **kwargs):
        """Serialize arguments to a string representation."""
        # cls is the instance's class, not the class's class
        serialized_args = [str(arg) for arg in args]
        serialized_kwargs = [str(kwargs), cls.__name__]
        serialized_args.extend(serialized_kwargs)
        return "".join(serialized_args)

    @staticmethod
    def delete_instance_func(self):
        """Replace the __del__ method of the class that uses this metaclass.

        Parameters
        ----------
        self : instance of the class that uses this metaclass
        """
        print("Bye bye instance of class {}!".format(self.__class__.__name__))

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.__del__ = PoolMeta.delete_instance_func

    def __del__(self):
        PoolMeta.delete_instance_func(self)

    # the same as assigning the following in the metaclass __init__
    # PoolMeta.__del__ = PoolMeta.delete_instance_func

    def __call__(cls, *args, **kwargs):
        print("\nMeta.__call__(cls={}, args={}, kwargs={})".format(cls, args, kwargs))
        key = PoolMeta.serialize_arguments(cls, *args, **kwargs)

        try:
            instance = PoolMeta.pool[key]
            print("Found in pool (skip __new__ and __init__)")
            del PoolMeta.pool[key]  # remove from pool
        except KeyError:
            print("Not found in pool")
            instance = super().__call__(*args, **kwargs)

        PoolMeta.pool[key] = instance  # insert in pool
        return instance


class A(object, metaclass=PoolMeta):

    def __new__(cls, *args, **kwargs):
        print("A.__new__")
        return super().__new__(cls)

    def __init__(self, x):
        print("A.__init__")
        self.x = x


class B(object, metaclass=PoolMeta):

    def __new__(cls, *args, **kwargs):
        print("B.__new__")
        return super().__new__(cls)

    def __init__(self, x):
        print("B.__init__")
        self.x = x


class C(B):

    def __new__(cls, *args, **kwargs):
        print("C.__new__")
        return super().__new__(cls)

    def __init__(self, x, y, z=123):
        super().__init__(x)
        print("C.__init__")
        self.x = x
        self.y = y
        self.z = z


def print_pool():
    print("Final state of the Pool (this function was registered with atexit)")
    pprint.pprint(PoolMeta.pool)
    print("")


def main():
    a1 = A(10)
    a2 = A(10)
    assert id(a1) == id(a2)
    a3 = A(42)
    assert id(a3) != id(a2)

    b1 = B(10)
    b2 = B(10)
    assert id(b1) == id(b2)
    c1 = C(1, 2, z=3)
    c2 = C(1, 2, 42)
    assert id(c1) != id(c2)

    assert type(PoolMeta) == type
    assert type(A) == PoolMeta
    assert type(B) == PoolMeta
    assert type(C) == PoolMeta


if __name__ == "__main__":
    atexit.register(print_pool)
    main()
    print("")
    print(A.__del__.__doc__)
