"""Borg pattern

Share state among instances.
"""


class Borg(object):
    """All instances of Borg share state with themselves and with all instances
    of Borg's subclasses, unless _shared_state is overriden in that class."""

    _shared_state = {}

    def __init__(self, name):
        self.__dict__ = self._shared_state
        if name is not None:
            self.name = name

    def __str__(self):
        cls = self.__class__.__name__
        return "Class: {}; ID: {}; state: {}".format(cls, id(self), self._shared_state)

    @property
    def state(self):
        return self._shared_state


class ChildShare(Borg):
    """All instances of ChildShare share state with themselves and with all
    instances of Borg."""

    def __init__(self, name=None, color=None):
        super().__init__(name)  # ok in Python 3.x, not in 2.x

        if color is not None:
            self.color = color


class ChildNotShare(Borg):
    """All instances of ChildNotShare share state with themselves, but not with
    instances of Borg or any of Borg's subclass. That's because we override
    _shared_state = {}.
    """
    _shared_state = {}

    def __init__(self, name=None, age=None):
        super(self.__class__, self).__init__(name)  # also ok in Python 2.x

        if age is not None:
            self.age = age


def main():
    print("2 instances of Borg")
    a = Borg("Mark")
    print(a)
    b = Borg("Luke")
    print(a)
    print(b)
    assert a is not b
    assert a.state is b.state

    print("\n1 instance of Borg and 1 of ChildShare")
    c = ChildShare("Paul", color="red")
    print(a)
    print(c)
    assert a.state is c.state

    print("\n1 instance of Borg, 1 of ChildShare, and 1 of ChildNotShare")
    d = ChildNotShare("Andrew", age=5)
    print(a)
    print(c)
    print(d)
    assert a.state is not d.state

    print("\n2 instances of ChildNotShare")
    e = ChildNotShare("Tom", age=7)
    print(d)
    print(e)
    assert d.state is e.state

    print("\nSet an attribute directly")
    a.name = "James"
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    assert a.name is c.name
    assert a.name is not d.name


if __name__ == "__main__":
    main()
