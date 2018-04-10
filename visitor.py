"""Visitor pattern

Visitor gives us the ability to add new operations to existing objects without
modifying these objects. It's one way to follow the open/closed principle.
"""


# classes that we cannot change (e.g. a fairly stable class hierarchy)


class Element(object):
    pass


class ElementOne(Element):
    pass


class ElementTwo(Element):
    pass


class ElementThree(ElementOne, ElementTwo):
    pass


class ElementFour(ElementThree):
    pass


# Extrinsic Visitor


class Visitor(object):

    operations = {
        "ElementTwo": "custom_operation", "ElementFour": "another_custom_operation"
    }

    def visit(self, element, *args, **kwargs):
        """Perform an operation specific for the passed element.

        Steps:
        1. traverse the class hierarchy of an Element object
        2. discover what operation to perform on the Element object
        3. perform the specific operation on the Element object

        Parameters
        ----------
        element : Element
            object whose behavior must be implemented here

        Returns
        -------
        return value/s of the method chosen at runtime
        """
        method_name = "default_operation"
        for cls in element.__class__.__mro__:
            try:
                method_name = self.operations[cls.__name__]
                break  # we found out a custom operation to perform, so we exit

            except KeyError:
                pass  # keep default_operation if there isn't a custom one
        method = getattr(self, method_name)
        return method(element, *args, **kwargs)

    # implement the behaviors for the Element objects

    @staticmethod
    def default_operation(elem, *args, **kwargs):
        print(
            "No custom operation defined for {} or its class hierarchy".format(
                elem.__class__.__name__
            )
        )
        print(
            "default_operation on {} with args {} and kwargs {}".format(
                elem.__class__.__name__, args, kwargs
            )
        )

    @staticmethod
    def custom_operation(elem, *args, **kwargs):
        print(
            "custom_operation on {} with args {} and kwargs {}".format(
                elem.__class__.__name__, args, kwargs
            )
        )

    @staticmethod
    def another_custom_operation(elem, *args, **kwargs):
        print(
            "another_custom_operation on {} with args {} and kwargs {}".format(
                elem.__class__.__name__, args, kwargs
            )
        )


def main():
    elements = [ElementOne(), ElementTwo(), ElementThree(), ElementFour()]
    visitor = Visitor()
    for elem in elements:
        visitor.visit(elem)


if __name__ == "__main__":
    main()
