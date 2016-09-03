import random
import inspect
from abc import ABC, abstractmethod


class Polygon(ABC):
    """Basic abstract class for polygons.

    Polygon (factory class) creates many different polygons (products) without
    exposing the instantiation logic to the client.
    Trying to instantiate an object of a Polygon subclass without implementing
    ALL abstract methods in the sublass itself will raise a TypeError exception.
    """
    def __str__(self):
        return '{} (perimeter: {}; area: {})'\
            .format(self.__class__.__name__, self.perimeter(), self.area())

    @abstractmethod
    def perimeter(self):
        """Compute the perimeter of the polygon. Implement in subclass."""
        pass

    @abstractmethod
    def area(self):
        """Compute the area of the polygon. Implement in subclass."""
        pass

    @staticmethod
    def factory_method(vertices):
        assert vertices >= 3, 'In Euclidean geometry a polygon has 3+ vertices!'
        if vertices == 3:
            triangle_type = random.choice(
                ['TriangleEquilateral', 'TriangleIsosceles', 'TriangleScalene'])
            this_module = __import__(__name__)
            class_ = getattr(this_module, triangle_type)
            return class_()
        elif vertices == 4:
            quadrilateral_type = random.choice(
                ['Square', 'Rectangle', 'ConvexQuadrilateral'])
            this_module = __import__(__name__)
            class_ = getattr(this_module, quadrilateral_type)
            return class_()
        else:
            # we could raise a NotImplementerError here
            return 'Currently we can\'t create a polygon with {} vertices'\
                .format(vertices)


class Triangle(Polygon):

    def perimeter(self):
        return 'a+b+c'

    def area(self):
        return 'b*h/2'


class TriangleEquilateral(Triangle):

    def perimeter(self):
        return '3a'


class TriangleIsosceles(Triangle):

    def perimeter(self):
        return '2a + b'


class TriangleScalene(Triangle):
    pass


class Quadrilateral(Polygon):

    def perimeter(self):
        return 'a+b+c+d'

    def area(self):
        return 'Bretschneider\'s formula'


class Square(Quadrilateral):

    def perimeter(self):
        return '4a'

    def area(self):
        return 'a * a'


class Rectangle(Quadrilateral):

    def perimeter(self):
        return '2a + 2b'

    def area(self):
        return 'a*b'


class ConvexQuadrilateral(Quadrilateral):
    pass


def vertices_generator(num_polygons):
    for i in range(num_polygons):
        # if we yield a number of vertices for which we did not implemented a
        # polygon class, the factory_method will not be able to create an object
        # (e.g. we can yield 5 here, but we didn't implement a Pentagon class).
        yield random.choice([3, 4, 5])


def main():
    n = 10  # number of polygons we wish to create
    polygons = [Polygon.factory_method(v) for v in vertices_generator(n)]
    for p in polygons:
        print('__str(self)__ (human-readable): {}'.format(str(p)))
        print('__repr(self)__ (machine-readable): {}'.format(repr(p)))
        print('Hierarchy of {}'.format(p.__class__.__name__))
        print(inspect.getmro(p.__class__))
        print('\n')


if __name__ == '__main__':
    main()
