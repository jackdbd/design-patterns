"""Bridge pattern

Bridge is a structural design pattern. It separates responsibilities into two
orthogonal class hierarchies: implementation and interface. Bridge decouples an
abstraction from its implementation so that the two can vary independently.

The interface class encapsulates an instance of a concrete implementation class.
The client interacts with the interface class, and the interface class in turn
"delegates" all requests to the implementation class.

Adapter makes things work after they're designed; Bridge makes them work before
they are.
"""
from abc import ABC, abstractmethod


# Abstract Interface (aka Handle) used by the client


class Website(ABC):

    def __init__(self, implementation):
        # encapsulate an instance of a concrete implementation class
        self._implementation = implementation

    def __str__(self):
        return "Interface: {}; Implementation: {}".format(
            self.__class__.__name__, self._implementation.__class__.__name__
        )

    @abstractmethod
    def show_page(self):
        pass


# Concrete Interface 1


class FreeWebsite(Website):

    def show_page(self):
        ads = self._implementation.get_ads()
        text = self._implementation.get_excerpt()
        call_to_action = self._implementation.get_call_to_action()
        print(ads)
        print(text)
        print(call_to_action)
        print("")


# Concrete Interface 2


class PaidWebsite(Website):

    def show_page(self):
        text = self._implementation.get_article()
        print(text)
        print("")


# Abstract Implementation (aka Body) decoupled from the client


class Implementation(ABC):

    def get_excerpt(self):
        return "excerpt from the article"

    def get_article(self):
        return "full article"

    def get_ads(self):
        return "some ads"

    @abstractmethod
    def get_call_to_action(self):
        pass


# Concrete Implementation 1


class ImplementationA(Implementation):

    def get_call_to_action(self):
        return "Pay 10 $ a month to remove ads"


# Concrete Implementation 2


class ImplementationB(Implementation):

    def get_call_to_action(self):
        return "Remove ads with just 10 $ a month"


# Client


def main():
    a_free = FreeWebsite(ImplementationA())
    print(a_free)
    a_free.show_page()

    b_free = FreeWebsite(ImplementationB())
    print(b_free)
    b_free.show_page()

    a_paid = PaidWebsite(ImplementationA())
    print(a_paid)
    a_paid.show_page()

    b_paid = PaidWebsite(ImplementationB())
    print(b_paid)
    b_paid.show_page()

    # in a real world scenario, we could perform A/B testing of our website by
    # choosing a random implementation
    import random

    impl = random.choice([ImplementationA(), ImplementationB()])
    print(FreeWebsite(impl))


if __name__ == "__main__":
    main()
