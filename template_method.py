"""Template method pattern

Template Method is a behavioral design pattern. It defines an algorithm's
skeleton in a Base class, but lets subclasses redefine certain steps of the
algorithm. The Base class declares some placeholder methods, and derived classes
implement them.
"""
import sys
from abc import ABC, abstractmethod


class Algorithm(ABC):

    def template_method(self):
        """Skeleton of operations to perform. DON'T override me.

        The Template Method defines a skeleton of an algorithm in an operation,
        and defers some steps to subclasses.
        """
        self.__do_absolutely_this()
        self.do_step_1()
        self.do_step_2()
        self.do_something()

    def __do_absolutely_this(self):
        """Protected operation. DON'T override me."""
        this_method_name = sys._getframe().f_code.co_name
        print("{}.{}".format(self.__class__.__name__, this_method_name))

    @abstractmethod
    def do_step_1(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def do_step_2(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    def do_something(self):
        """Hook. You CAN override me, I'm NOT a placeholder."""
        print("do something")


class AlgorithmA(Algorithm):

    def do_step_1(self):
        print("do step 1 for Algorithm A")

    def do_step_2(self):
        print("do step 2 for Algorithm A")


class AlgorithmB(Algorithm):

    def do_step_1(self):
        print("do step 1 for Algorithm B")

    def do_step_2(self):
        print("do step 2 for Algorithm B")

    def do_something(self):
        print("do something else")


def main():
    print("Algorithm A")
    a = AlgorithmA()
    a.template_method()

    print("\nAlgorithm B")
    b = AlgorithmB()
    b.template_method()


if __name__ == "__main__":
    main()
