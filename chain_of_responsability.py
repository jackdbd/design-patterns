"""Chain of responsability pattern
"""
from abc import ABC
import random


class CannotHandleRequest(Exception):
    pass


class Node(ABC):

    def __init__(self):
        self._next_node = None

    def __str__(self):
        return "{}".format(self.__class__.__name__)

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, node):
        self._next_node = node

    def handle(self, request, *args, **kwargs):
        req_name = request["name"]
        req_args = request["args"]
        req_kwargs = request["kwargs"]
        method_name = "{}".format(req_name)

        try:
            method = getattr(self, method_name)
        except AttributeError:
            if self._next_node is None:
                raise CannotHandleRequest(
                    'The request "{}" could not be handled by any node in the '
                    "chain".format(req_name)
                )

            else:
                print(
                    'The request "{}" cannot be handled by {}. Pass request '
                    "to {}".format(req_name, str(self), str(self.next_node))
                )
                self._next_node.handle(request, *args, **kwargs)
        else:
            print(
                '{} handles request "{}" with arguments {} and keywords {}'.format(
                    str(self), req_name, req_args, req_kwargs
                )
            )
            method(request, *args, **kwargs)


class WatcherNode(Node):

    def watch(self, request, *args, **kwargs):
        # implement actual behavior here
        string = "Process request {}".format(request)
        if args:
            string += " extra arguments {}".format(args)
        if kwargs:
            string += " extra keywords {}".format(kwargs)
        print(string)


class BuyerNode(Node):

    def buy(self, request, *args, **kwargs):
        # implement actual behavior here
        string = "Process request {}".format(request)
        if args:
            string += " extra arguments {}".format(args)
        if kwargs:
            string += " extra keywords {}".format(kwargs)
        print(string)


class EaterNode(Node):

    def eat(self, request, *args, **kwargs):
        # implement actual behavior here
        string = "Process request {}".format(request)
        if args:
            string += " extra arguments {}".format(args)
        if kwargs:
            string += " extra keywords {}".format(kwargs)
        print(string)


def create_chain(*args):
    chain = list()
    for i, node in enumerate(args):
        if i < len(args) - 1:
            node.next_node = args[i + 1]
        chain.append(node)
    return chain


def request_generator():
    available_requests = ["buy", "watch", "eat"]
    available_args = [(), (123,), (42, 10)]
    available_kwargs = [{}, {"movie": "Hero"}, {"apple": 3, "color": "red"}]
    req_num = random.choice([3, 4, 5])
    for i in range(req_num):
        req_name = random.choice(available_requests)
        req_args = random.choice(available_args)
        req_kwargs = random.choice(available_kwargs)
        request = {"name": req_name, "args": req_args, "kwargs": req_kwargs}
        yield request


# Client


def main():
    # Client (or a third party) defines a chain of nodes (handlers) at runtime
    chain = create_chain(EaterNode(), BuyerNode(), WatcherNode())
    root_node = chain[0]
    for i, req in enumerate(request_generator()):
        print("Request {}".format(i + 1))
        root_node.handle(req)
        print("Request {} with extra arguments/keywords".format(i + 1))
        root_node.handle(req, 1, 34, key1=44, greet="hello")
        print("")


if __name__ == "__main__":
    main()
