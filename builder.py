"""Builder pattern

The Builder pattern separates the construction of a complex object from its
representation so that the same construction process can create different
representations.
"""
from abc import ABC, abstractmethod


class IceCream(ABC):
    """Abstract Product."""

    @property
    def need_spoon(self):
        return False

    def __str__(self):
        string = self.__class__.__name__
        for key, value in self.__dict__.items():
            string += "\n{}: {}".format(key, value)
        string += "\n"
        return string


class ConeIceCream(IceCream):
    """Concrete Product 1."""
    pass


class CupIceCream(IceCream):
    """Concrete Product 2."""

    @property
    def need_spoon(self):
        return True


class Builder(ABC):
    """Specify the abstract interface that creates all parts of the product.

    This Abstract interface is used by a Director object. All methods except
    "get_product" return self, so this class is a "fluent interface".
    """

    @abstractmethod
    def __init__(self):
        self.product = None
        self.toppings = None

    def set_flavors(self, flavors):
        self.product.flavors = flavors
        return self

    def set_toppings(self):
        if self.toppings is not None:
            self.product.toppings = self.toppings
        return self

    def add_spoon(self):
        if self.product.need_spoon:
            self.product.spoon = 1
        return self

    def get_product(self):
        return self.product


class ConeIceCreamBuilder(Builder):
    """Concrete Builder 1.

    This class assembles the product by implementing the Builder interface.
    It defines and keeps track of the representation it creates.
    """

    def __init__(self):
        # super().__init__()  # ok in Python 3.x, not in 2.x
        super(self.__class__, self).__init__()  # also ok in Python 2.x
        self.product = ConeIceCream()
        self.toppings = "hazelnuts"


class CupIceCreamBuilder(Builder):
    """Concrete Builder 2.

    This class assembles the product by implementing the Builder interface.
    It defines and keeps track of the representation it creates.
    """

    def __init__(self):
        # super().__init__()  # ok in Python 3.x, not in 2.x
        super(self.__class__, self).__init__()  # also ok in Python 2.x
        self.product = CupIceCream()
        self.toppings = "chocolate chips"


class Director(object):
    """Build an object using the Builder interface."""

    def __init__(self, builder):
        self.builder = builder

    def build_product(self, flavors):
        """Prepare the product and finally return it to the client.

        The Builder class defined above is a "fluent interface", so we can use
        method chaining.

        Parameters
        ----------
        flavors : list

        Returns
        -------
        ConeIceCream or CupIceCream
        """
        return self.builder.set_flavors(
            flavors
        ).set_toppings().add_spoon().get_product()


# Client: it creates a Director object and configures it with a Builder object.


def main():
    director = Director(ConeIceCreamBuilder())
    product = director.build_product(["chocolate", "vanilla", "banana"])
    print(product)

    director = Director(CupIceCreamBuilder())
    product = director.build_product(["lemon", "strawberry"])
    print(product)

    builder = ConeIceCreamBuilder()
    director = Director(builder)
    builder.toppings = None  # the ConeIceCreamBuilder has no more toppings!
    product = director.build_product(["chocolate", "vanilla", "banana"])
    print(product)


if __name__ == "__main__":
    main()
