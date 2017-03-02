"""Factory Method pattern
"""


class _Car(object):
    pass


class _Bike(object):
    pass


def factory_method(product_type):
    if product_type == 'car':
        return _Car()
    elif product_type == 'bike':
        return _Bike()
    else:
        raise ValueError('Cannot make: {}'.format(product_type))


def main():
    for product_type in ('car', 'bike'):
        product = factory_method(product_type)
        print(str(product))

if __name__ == '__main__':
    main()
