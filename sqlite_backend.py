"""Some tests with the db-sqlite3 module.

Documentation:
https://www.sqlite.org/datatype3.html
https://docs.python.org/3/library/sqlite3.html
"""
import sqlite3


def create_db(db_name):
    """Create a sqlite database and return a connection.

    Parameters
    ----------
    db_name : str
        database name

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    connection = sqlite3.connect('{}.db'.format(db_name))
    return connection


def create_table(cursor, table_name):
    cursor.execute('CREATE TABLE {} (name TEXT, price FLOAT, quantity INT)'
                   .format(table_name))


def insert_one(cursor, item, table_name):
    cursor.execute(
        "INSERT INTO {} VALUES ('{}', {}, {})"
        .format(table_name, item['name'], item['price'], item['quantity']))


def insert_many(cursor, items, table_name):
    entries = list()
    for x in items:
        entries.append((x['name'], x['price'], x['quantity']))
    cursor.executemany('INSERT INTO {} VALUES (?, ?, ?)'
                       .format(table_name), entries)


def sample_item():
    return {'name': 'milk', 'price': 1.5, 'quantity': 4}


def sample_items():
    return [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'eggs', 'price': 0.2, 'quantity': 100},
        {'name': 'cheese', 'price': 2.5, 'quantity': 20},
    ]


def main():
    conn = create_db('MyDB')
    c = conn.cursor()
    create_table(c, 'items')

    insert_one(c, sample_item(), table_name='items')
    insert_many(c, sample_items(), 'items')

    # save (commit) the changes
    conn.commit()

    # close connection
    conn.close()

if __name__ == '__main__':
    main()
