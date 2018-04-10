"""Iterator pattern
"""


class MyIterator(object):

    def __init__(self, *args):
        self.data = args
        self.index = 0

    def __iter__(self):
        generator = self.generator_function()
        return generator

    def __next__(self):
        if len(self.data) > self.index:
            obj = self.data[self.index]
            self.index += 1
        else:
            raise StopIteration("No more elements!")

        return obj

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data[self.index:])

    def generator_function(self):
        for d in self.data[self.index:]:
            self.index += 1
            yield "Item: {} (type: {})".format(d, type(d))


def some_function(a, b, c=123):
    print(a, b, c)


def main():
    iterator = MyIterator(1, 3.0, None, "hello", some_function)
    print("Initial length")
    print(len(iterator))

    index = 3
    print("\nGet item at index {}".format(index))
    print(iterator[index])

    print("\n__next__ calls")
    print(next(iterator))
    print(next(iterator))

    print("\nLength after __next__ calls")
    print(len(iterator))

    print("\nFor loop with the remaining items")
    for item in iterator:
        print(item)

    print("\nStopIteration")
    try:
        next(iterator)
    except StopIteration as e:
        print(e)

    print("But in Python we don't really need any of the above...")
    for item in (1, 3.0, None, "hello", some_function):
        print(item)


if __name__ == "__main__":
    main()
