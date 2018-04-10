"""Decorator pattern

Decorator is a structural design pattern. It is used to extend (decorate) the
functionality of a certain object at run-time, independently of other instances
of the same class.
The decorator pattern is an alternative to subclassing. Subclassing adds
behavior at compile time, and the change affects all instances of the original
class; decorating can provide new behavior at run-time for selective objects.
"""


class Component(object):

    # method we want to decorate

    def whoami(self):
        print("I am {}".format(id(self)))

    # method we don't want to decorate

    def another_method(self):
        print("I am just another method of {}".format(self.__class__.__name__))


class ComponentDecorator(object):

    def __init__(self, decoratee):
        self._decoratee = decoratee  # reference of the original object

    def whoami(self):
        print("start of decorated method")
        self._decoratee.whoami()
        print("end of decorated method")

    # forward all "Component" methods we don't want to decorate to the
    # "Component" pointer

    def __getattr__(self, name):
        return getattr(self._decoratee, name)


def main():
    a = Component()  # original object
    b = ComponentDecorator(a)  # decorate the original object at run-time
    print("Original object")
    a.whoami()
    a.another_method()
    print("\nDecorated object")
    b.whoami()
    b.another_method()


if __name__ == "__main__":
    main()
