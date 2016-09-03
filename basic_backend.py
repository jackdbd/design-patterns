items = list()


def create_items():
    global items
    items = [
        {'name': 'milk', 'price': 1.50, 'quantity': 10},
        {'name': 'eggs', 'price': 0.20, 'quantity': 100},
        {'name': 'cheese', 'price': 2.00, 'quantity': 10},
    ]


def read_item(name):
    global items
    return list(filter(lambda x: x['name'] == name, items))


def read_items():
    global items
    return [item for item in items]


def update_item(item):
    global items
    # Python 3.x removed tuple parameters unpacking (PEP 3113), so we have to do
    # it manually (i_x is a tuple, idxs_items is a list of tuples)
    idxs_items = list(
        filter(lambda i_x: i_x[1]['name'] == item['name'], enumerate(items)))
    i, item_to_update = idxs_items[0][0], idxs_items[0][1]
    items[i] = item


def delete_item(name):
    global items
    # Python 3.x removed tuple parameters unpacking (PEP 3113), so we have to do
    # it manually (i_x is a tuple, idxs_items is a list of tuples)
    idxs_items = list(
        filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))
    i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
    del items[i]


def main():

    # CREATE
    create_items()

    # READ
    print('READ items')
    print(read_items())
    print('READ strawberry')
    print(read_item('strawberry'))
    print('READ milk')
    print(read_item('milk'))

    # UPDATE
    print('UPDATE milk')
    update_item({'name': 'milk', 'price': 2.0, 'quantity': 30})
    print(read_item('milk'))

    # DELETE
    print('DELETE cheese')
    delete_item('cheese')

    print('READ items')
    print(read_items())

if __name__ == '__main__':
    main()
