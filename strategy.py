"""Strategy pattern

Strategy is a behavioral design pattern.
"""
from abc import ABC, abstractmethod


class StrategyInterface(ABC):
    """Common interface for all strategies."""

    @abstractmethod
    def compute_area(self):
        pass


class SquareStrategy(StrategyInterface):

    def compute_area(self):
        print('Compute area of a square')


class RectangleStrategy(StrategyInterface):

    def compute_area(self):
        print('Compute area of a rectangle')


class Context(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def compute_area(self):
        return self.strategy.compute_area()


def main():
    c1 = Context(SquareStrategy())
    c1.compute_area()
    c2 = Context(RectangleStrategy())
    c2.compute_area()

if __name__ == '__main__':
    main()
