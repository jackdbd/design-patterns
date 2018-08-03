"""Closure pattern

A closure is a record storing a function together with an environment.
"""


def outer(x):
    def inner(y):
        return x + y

    return inner


def outer2(x):
    def inner2(y, x=x):
        return x + y

    return inner2


def main():
    # inner is defined in the local scope of outer, so we can't access it
    try:
        inner()
    except NameError as e:
        print(e)

    # a closure
    func = outer(3)
    print(func(2))

    # func stores inner and the environment where inner was defined
    assert func.__name__ == "inner"
    # in inner's scope x was not defined, but it was - and still is - available
    # in its environment, so we can access x
    assert func.__code__.co_freevars[0] == "x"
    # so func is a closure
    assert func.__closure__ is not None

    # just a nested function, not a closure
    func2 = outer2(3)
    print(func2(2))

    # func2 stores inner2 and the environment where inner2 was defined
    assert func2.__name__ == "inner2"
    # in inner2's scope x was (re)defined (variable shadowing), so it's not a
    # free variable
    assert not func2.__code__.co_freevars
    # so func2 is NOT a closure
    assert func2.__closure__ is None


if __name__ == "__main__":
    main()
