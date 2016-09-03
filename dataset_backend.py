"""Some tests with the dataset module.

https://dataset.readthedocs.io/en/latest/
"""
import dataset
import mvc_exceptions as mvc_exc


INSERT_SUCCESS = 1
INSERT_FAIL = 0


def create_db():
    return dataset.connect('sqlite:///:memory:')


def create_table(db, table_name):
    return db[table_name]


def insert_sample_items(table):
    items = [
        {'name': 'milk', 'price': 1.0, 'quantity': 5},
        {'name': 'eggs', 'price': 0.2, 'quantity': 100},
        {'name': 'cheese', 'price': 2.5, 'quantity': 20}
    ]
    try:
        for item in items:
            table.insert(dict(name=item['name'], price=item['price'],
                              quantity=item['quantity']))
        response_code = INSERT_SUCCESS
    except Exception:
        response_code = INSERT_FAIL
    return response_code


def insert(item, db, table):
    try:
        table.insert(dict(
            name=item['name'], price=item['price'], quantity=item['quantity']))
        print('INSERT operation succeeded. {} inserted into {}.{}'
              .format(item, db.url, table.table.name))
        response_code = INSERT_SUCCESS
    except (TypeError, KeyError) as e:
        print('INSERT operation failed. You tried to insert {} into {}.{}'
              .format(item, db.url, table.table.name))
        response_code = INSERT_FAIL
    return response_code


def get_all_records(table):
    rows = table.all()
    return rows


def main():
    db = create_db()
    table = create_table(db, 'items')
    response = insert_sample_items(table)
    items = get_all_records(table)
    for row in items:
        print(row['name'], row['price'], row['quantity'])

    # there is no chocolate, so find_one returns None
    print(table.find_one(name='chocolate'))
    # insert chocolate
    insert({'name': 'chocolate', 'price': 2.5, 'quantity': 10}, db, table)
    # now there is chocolate, so find_one returna an OrderedDict
    print(table.find_one(name='chocolate'))

if __name__ == '__main__':
    main()
