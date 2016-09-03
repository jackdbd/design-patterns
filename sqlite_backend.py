"""SQLite backend (db-sqlite3).

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
https://www.sqlite.org/datatype3.html
https://docs.python.org/3/library/sqlite3.html
"""
import sqlite3
from sqlite3 import OperationalError, IntegrityError

DB_name = 'myDB'
# DB_name = ':memory:'  # in-memory database

# TODO: check how to handle connections. Right now each CRUD operation can create
# a db connection, but it doesn't close it. Maybe we'd like to keep the db
# connection open if it is passed as argument, and close it only if it wasn't
# passed (namely if we had to open it in the function itself).


def connect_to_db(db=None):
    """Connect to a sqlite DB. Create the database if there isn't one yet.

    Opens a connection to a SQLite DB (either a DB file or an in-memory DB).
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    db : str
        database name (without .db extension). If None, create an In-Memory DB.

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    if db is None:
        mydb = ':memory:'
    else:
        mydb = '{}.db'.format(db)
    connection = sqlite3.connect(mydb)
    return connection


def create_table(table_name, conn=None):
    sql = 'CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'name TEXT UNIQUE, price REAL, quantity INTEGER)'.format(table_name)
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    try:
        c.execute(sql)
        conn.commit()  # is it really needed?
    except OperationalError as e:
        print(e)


def insert_one(item, table_name, conn=None):
    sql = "INSERT INTO {} ('name', 'price', 'quantity') VALUES ('{}', {}, {})"\
        .format(table_name, item['name'], item['price'], item['quantity'])
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    try:
        c.execute(sql)
        conn.commit()
    except IntegrityError as e:
        print('{}: {} already stored in {}'.format(e, item['name'], table_name))


def insert_many(items, table_name, conn=None):
    sql = "INSERT INTO {} ('name', 'price', 'quantity') VALUES (?, ?, ?)"\
        .format(table_name)
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    entries = list()
    for x in items:
        entries.append((x['name'], x['price'], x['quantity']))
    try:
        c.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in {}'
              .format(e, [x['name'] for x in items], table_name))


def select_one(item_name, table_name, conn=None):
    sql = 'SELECT * FROM {} WHERE name="{}"'.format(table_name, item_name)
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    c.execute(sql)
    return c.fetchone()


def select_all(table_name, conn=None):
    sql = 'SELECT * FROM {}'.format(table_name)
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    c.execute(sql)
    return c.fetchall()


def update_one(item, table_name, conn=None):
    sql = 'UPDATE {} SET price = {}, quantity={} WHERE name="{}"'\
        .format(table_name, item['price'], item['quantity'], item['name'])
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()


def delete_one(item_name, table_name, conn=None):
    sql = 'DELETE FROM {} WHERE name="{}"'.format(table_name, item_name)
    if conn is None:
        conn = connect_to_db(DB_name)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()


def sample_item():
    return {'name': 'milk', 'price': 1.5, 'quantity': 4}


def sample_items():
    return [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'eggs', 'price': 0.2, 'quantity': 100},
        {'name': 'cheese', 'price': 2.5, 'quantity': 20},
    ]


def main():
    conn = connect_to_db(DB_name)
    create_table('items')

    # CREATE
    insert_one(sample_item(), table_name='items', conn=conn)
    insert_many(sample_items(), table_name='items', conn=conn)
    insert_one(sample_item(), table_name='items', conn=conn)

    # READ
    print('SELECT milk')
    print(select_one('milk', table_name='items', conn=conn))
    print('SELECT all')
    print(select_all(table_name='items', conn=conn))

    # UPDATE
    print('UPDATE bread, SELECT bread')
    update_one({'name': 'bread', 'price': 1.5, 'quantity': 5},
               table_name='items', conn=conn)
    print(select_one('bread', table_name='items', conn=conn))

    # DELETE
    print('DELETE milk, SELECT all')
    delete_one('milk', table_name='items', conn=conn)
    print(select_all(table_name='items', conn=conn))

    # save (commit) the changes
    # conn.commit()

    # close connection
    conn.close()

if __name__ == '__main__':
    main()
