"""Strategy pattern

Strategy is a behavioral design pattern. It enables an algorithm's behavior to
be selected at runtime. We can implement it by creating a common (abstract)
interface and subclassing it with a new class for each strategy, how it's done
in [1], or by creating a single class and replacing a method of that class with
a different function, how it's done in [2]. The latter implementation is
possible because in Python functions are first class objects.
"""
import types


class Strategy(object):

    def __init__(self, func=None):

        if func is not None:
            # replace the default bound method 'execute' with a simple function.
            # The new 'execute' method will be a static method (no self).
            # self.execute = func
            # take a function, bind it to this instance, and replace the default
            # bound method 'execute' with this new bound method.
            # The new 'execute' will be a normal method (self available).
            self.execute = types.MethodType(func, self)
            self.name = "{}_{}".format(self.__class__.__name__, func.__name__)
        else:
            self.name = "{}_default".format(self.__class__.__name__)

    def execute(self):
        print("Default method")
        print("{}\n".format(self.name))


# Replacement strategies for the default method 'execute'. These ones are
# defined as normal functions, so we will need to bind them to an instance when
# the object is instatiated (we can use types.MethodType).


def execute_replacement1(self):
    print("Replacement1 method")
    print("{}\n".format(self.name))


def execute_replacement2(self):
    print("Replacement2 method")
    print("{}\n".format(self.name))


def main():

    # This part of the program is the Context: it decides which strategy to use.

    s0 = Strategy()
    s0.execute()

    s1 = Strategy(execute_replacement1)
    s1.execute()

    s2 = Strategy(execute_replacement2)
    s2.execute()


if __name__ == "__main__":
    main()
