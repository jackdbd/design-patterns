import random
import inspect
from abc import ABC, abstractmethod


class PolygonFactory(ABC):
    """Basic abstract Factory class for making polygons (products).

    This class has to be sublassed by a factory class that MUST implement
    the "products" method.
    A factory class can create many different polygon objects (products) without
    exposing the instantiation logic to the client. Infact, since all methods of
    this class are abstract, this class can't be instantiated at all! Also, each
    subclass of PolygonFactory should implement the "products" method and keep
    it abstract, so even that subclass can't be instatiated.
    """

    @classmethod
    @abstractmethod
    def products(cls):
        """Products that the factory can manufacture. Implement in subclass."""
        pass

    @classmethod
    @abstractmethod
    def make_polygon(cls, color=None):
        """Instantiate a random polygon from all the ones that are available.

        This method creates an instance of a product randomly chosen from all
        products that the factory class can manufacture. The 'color' property of
        the manufactured object is reassigned here. Then the object is returned.

        Parameters
        ----------
        color : str
            color to assign to the manufactured object. It replaces the color
            assigned by the factory class.

        Returns
        -------
        polygon : an instance of a class in cls.products()
            polygon is the product manufactured by the factory class. It's one
            of the products that the factory class can make.
        """
        product_name = random.choice(cls.products())
        this_module = __import__(__name__)
        polygon_class = getattr(this_module, product_name)
        polygon = polygon_class(factory_name=cls.__name__)
        if color is not None:
            polygon.color = color
        return polygon

    @classmethod
    @abstractmethod
    def color(cls):
        return "black"


class TriangleFactory(PolygonFactory):
    """Abstract Factory class for making triangles."""

    @classmethod
    @abstractmethod
    def products(cls):
        return tuple(["_TriangleEquilateral", "_TriangleIsosceles", "_TriangleScalene"])


class QuadrilateralFactory(PolygonFactory):
    """Abstract Factory class for making quadrilaterals."""

    @classmethod
    @abstractmethod
    def products(cls):
        return tuple(["_Square", "_Rectangle", "_ConvexQuadrilateral"])


class _Polygon(ABC):
    """Basic abstract class for polygons.

    This class is private because the client should not try to instantiate it.
    The instantiation process should be carried out by a Factory class.
    A _Polygon subclass MUST override ALL _Polygon's abstract methods, otherwise
    a TypeError will be raised as soon as we try to instantiate that subclass.
    """

    def __init__(self, factory_name=None):
        self._color = "black"
        self._manufactured = factory_name

    def __str__(self):
        return "{} {} manufactured by {} (perimeter: {}; area: {})".format(
            self.color,
            self.__class__.__name__,
            self.manufactured,
            self.perimeter,
            self.area,
        )

    @property
    @abstractmethod
    def family(self):
        pass

    @property
    @abstractmethod
    def perimeter(self):
        pass

    @property
    @abstractmethod
    def area(self):
        pass

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    @property
    def manufactured(self):
        return self._manufactured

    @manufactured.setter
    def manufactured(self, factory_name):
        self._manufactured = factory_name


class _Triangle(_Polygon):
    """Basic concrete class for triangles."""

    @property
    def family(self):
        return "Triangles"

    @property
    def perimeter(self):
        return "a+b+c"

    @property
    def area(self):
        return "base*height/2"


class _TriangleEquilateral(_Triangle):

    @property
    def perimeter(self):
        return "3a"


class _TriangleIsosceles(_Triangle):

    @property
    def perimeter(self):
        return "2a+b"


class _TriangleScalene(_Triangle):
    pass


class _Quadrilateral(_Polygon):
    """Basic concrete class for quadrilaterals."""

    @property
    def family(self):
        return "Quadrilaterals"

    @property
    def perimeter(self):
        return "a+b+c+d"

    @property
    def area(self):
        return "Bretschneider's formula"


class _Square(_Quadrilateral):

    @property
    def perimeter(self):
        return "4a"

    @property
    def area(self):
        return "a*a"


class _Rectangle(_Quadrilateral):

    @property
    def perimeter(self):
        return "2a+2b"

    @property
    def area(self):
        return "base*height"


class _ConvexQuadrilateral(_Quadrilateral):
    pass


def give_me_some_polygons(factories, color=None):
    """Interface between the client and a Factory class.

    Parameters
    ----------
    factories : list, or abc.ABCMeta
        list of factory classes, or a factory class
    color : str
        color to pass to the manufacturing method of the factory class.

    Returns
    -------
    products : list
        a list of objects manufactured by the Factory classes specified
    """
    if not hasattr(factories, "__len__"):
        factories = [factories]

    products = list()
    for factory in factories:
        num = random.randint(5, 10)
        for i in range(num):
            product = factory.make_polygon(color)
            products.append(product)

    return products


def print_polygon(polygon, show_repr=False, show_hierarchy=False):
    print(str(polygon))
    if show_repr:
        print(repr(polygon))
    if show_hierarchy:
        print(inspect.getmro(polygon.__class__))
        print("\n")


def main():
    print("Let's start with something simple: some triangles")
    triangles = give_me_some_polygons(TriangleFactory)
    print("{} triangles".format(len(triangles)))
    for triangle in triangles:
        print_polygon(triangle)

    print("\nuse a different factory and add a color")
    quadrilaterals = give_me_some_polygons(QuadrilateralFactory, color="blue")
    print("{} quadrilaterals".format(len(quadrilaterals)))
    for quadrilateral in quadrilaterals:
        print_polygon(quadrilateral)

    print("\nand now a mix of everything. And all in red!")
    factories = [TriangleFactory, QuadrilateralFactory]
    polygons = give_me_some_polygons(factories, color="red")
    print("{} polygons".format(len(polygons)))
    for polygon in polygons:
        print_polygon(polygon)

    print(
        "we can still instantiate directly any subclass of _Polygon (but we "
        "shouldn't because they are private)"
    )
    print_polygon(_Square())
    print("we can't instantiate _Polygon because it has abstract methods.")


if __name__ == "__main__":
    main()
