"""Composite pattern
"""
from abc import ABC, abstractmethod


class Component(ABC):

    def __init__(self, name):
        self.name = name
        self.level = 0
        self.indentation = ""

    @abstractmethod
    def traverse(self):
        """Print the name of this component and all of its children.

        Implement in Composite and Leaf
        """
        pass


class Leaf(Component):

    def traverse(self):
        print("{}{}".format(self.indentation, self.name))


class Composite(Component):

    def __init__(self, name):
        # super().__init__(name)  # ok in Python 3.x, not in 2.x
        super(self.__class__, self).__init__(name)  # also ok in Python 2.x
        self.children = list()

    # we can design the "child management" interface here (we have safety,
    # namely a client cannot append/remove a child from a Leaf), or design such
    # interface in the Component class (we have transparency, but a client
    # could try to perform meaningless things like appending a node to a Leaf)

    def append_child(self, child):
        child.level = self.level + 1
        child.indentation = " " * child.level * 2
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def traverse(self):
        print("{}{}".format(self.indentation, self.name))
        [x.traverse() for x in self.children]


def main():
    c0 = Composite("/")
    l0 = Leaf("hello.txt")
    l1 = Leaf("readme.txt")
    c1 = Composite("home")
    c0.append_child(l0)
    c0.append_child(l1)
    c0.append_child(c1)

    l2 = Leaf("notes.txt")
    l3 = Leaf("todo.txt")
    c2 = Composite("documents")
    c1.append_child(l2)
    c1.append_child(l3)
    c1.append_child(c2)

    l4 = Leaf("draft.txt")
    c2.append_child(l4)

    print("Traverse the entire directory tree")
    c0.traverse()

    print('\nRemove "todo.txt" and traverse the tree once again')
    c1.remove_child(l3)
    c0.traverse()

    print('\nRemove "home" and traverse the tree once again')
    c0.remove_child(c1)
    c0.traverse()


if __name__ == "__main__":
    main()
