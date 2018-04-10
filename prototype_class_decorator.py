"""Prototype pattern
"""
from copy import deepcopy


class InstanceNotAvailable(Exception):
    pass


def prototype(hash_function=id, auto_register=False, debug=False):
    """Implement the Prototype pattern on a class.

    The decorated class gains the following methods:
      - register
      - unregister
      - clone (@classmethod)
      - identifier (@property)
      - available_identifiers (@staticmethod)

    Parameters
    ----------
    hash_function : function
        a function
    auto_register : bool
        if True, automatically add objects to instance pool at instantiation
    debug : bool
        if True, show some documentation while using this decorator

    Returns
    -------
    inner : function
    """

    def inner(klass):
        instance_pool = dict()

        class Decorated(klass):

            def __init__(self, *args, **kwargs):
                """Call __init__ of original class and assign an identifier.

                Parameters
                ----------
                args : tuple
                    args to pass to the __init__ of the original class
                kwargs : dict
                    kwarg to pass to the __init__ of the original class
                """
                klass.__init__(self, *args, **kwargs)
                self._identifier = hash_function(self)

            def __repr__(self, *args, **kwargs):
                klass_repr = klass.__repr__(self, *args, **kwargs)
                return "{} (id: {})".format(klass_repr, self.identifier)

            def register(self):
                """Add this instance to the instance pool."""
                instance_pool.update({self.identifier: self})
                if debug:
                    print("{} registered".format(self.identifier))

            def unregister(self):
                """Remove this instance from the instance pool."""
                if debug:
                    print("{} unregistered".format(self.identifier))
                del instance_pool[self.identifier]

            @property
            def identifier(self):
                """Return the identifier of this instance."""
                return self._identifier

            @identifier.setter
            def identifier(self, value):
                self._identifier = value

        Decorated.__name__ = klass.__name__

        class ClassObject:

            def __repr__(self):
                return klass.__name__

            __str__ = __repr__

            def __call__(self, *args, **kwargs):
                if debug:
                    print("{}.__call__ (prototype)".format(str(self)))
                decorated_instance = Decorated(*args, **kwargs)
                if auto_register:
                    decorated_instance.register()
                return decorated_instance

            @classmethod
            def clone(cls, identifier):
                """Get an instance from the pool and return it to the caller.

                Parameters
                ----------
                identifier : int
                    identifier for an instance

                Raises
                ------
                InstanceNotAvailable
                    if the instance is not available in the instance pool

                Returns
                -------
                cloned_obj : decorated class
                    instance of the decorated class
                """
                try:
                    original_object = instance_pool[identifier]
                    cloned_obj = deepcopy(original_object)
                    return cloned_obj

                except KeyError:
                    raise InstanceNotAvailable(
                        "Instance with identifier {} not found.\nWas it "
                        "registered?\nThe available identifiers are: {}".format(
                            identifier, cls.available_identifiers()
                        )
                    )

            @staticmethod
            def available_identifiers():
                """Return the identifiers stored in the instance pool.

                Returns
                -------
                list
                    identifiers of all instances available in instance pool.
                """
                return list(instance_pool.keys())

        return ClassObject()

    return inner


@prototype(hash_function=id)
class Point(object):

    def __init__(self, x, y):
        print("{}__init__ (original class)".format(self.__class__.__name__))
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.x, self.y)

    def move(self, x, y):
        self.x += x
        self.y += y


# TODO: how can we inherit from Point?

# we will decorate this class later


class Stuff(object):
    pass


class MoreStuff(Stuff):
    pass


def main():
    print("\nCreate 2 points")
    print("p1")
    p1 = Point(x=3, y=5)
    print(p1)
    print("p2")
    p2 = Point(x=100, y=150)
    print(p2)
    print("p1.identifier != p2.identifier")
    assert p1.identifier != p2.identifier

    print("\nIdentifiers in the instance pool")
    print(Point.available_identifiers())

    print(
        "\nThe instance pool is empty because we didn't register any "
        "instance. Let's fix this"
    )
    p1.register()
    p2.register()
    print(Point.available_identifiers())

    print("\nCreate a point by cloning p1 (__init__ is not called)")
    p3 = Point.clone(p1.identifier)
    print(p3)
    print("Create a point by cloning p3 (which is a clone of p1)")
    p4 = Point.clone(p3.identifier)
    print(p4)
    print("p1.identifier == p3.identifier == p4.identifier")
    assert p1.identifier == p3.identifier == p4.identifier

    print("\nIdentifiers in the instance pool")
    print(Point.available_identifiers())

    print("\nmove p1")
    p1.move(5, 7)
    print(p1)
    # p3 and p4 are not weak references of p1, they are deep copies
    print("if p1 moves, p3 and p4 are unaffected")
    print(p3)
    print(p4)

    print("\nunregister p1")
    p1.unregister()
    print("p1 cannot be cloned because it was unregistered")
    try:
        Point.clone(p1.identifier)
    except InstanceNotAvailable as e:
        print(e)
    print("but p1 still exists")
    print(p1)

    # TODO: this behavior might be undesirable
    print(
        "\nEven if we destroy p2, it's not removed from the instance pool, "
        "so if we know the identifier we can still clone it"
    )
    identifier = deepcopy(p2.identifier)
    del p2
    print(Point.available_identifiers())
    Point.clone(identifier)

    print("\nwith a wrong identifier we get a ValueError exception")
    wrong_identifier = 123456789
    try:
        Point.clone(wrong_identifier)
    except InstanceNotAvailable as e:
        print(e)

    print("\nDecorate a new class")
    proto = prototype(auto_register=True, debug=True)
    StuffDecorated = proto(Stuff)

    s1 = StuffDecorated()
    StuffDecorated.clone(s1.identifier)
    print("\nInstance pools are different for each class")
    print("StuffDecorated.available_identifiers")
    print(StuffDecorated.available_identifiers())
    print("Point.available_identifiers")
    print(Point.available_identifiers())

    proto = prototype(auto_register=True)
    MoreStuffDecorated = proto(MoreStuff)
    MoreStuffDecorated()
    print("MoreStuffDecorated.available_identifiers")
    print(MoreStuffDecorated.available_identifiers())


if __name__ == "__main__":
    main()
