"""SQLite backend (db-sqlite3).

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
https://www.sqlite.org/datatype3.html
https://docs.python.org/3/library/sqlite3.html
"""
import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import mvc_exceptions as mvc_exc
import mvc_mock_objects as mock


DB_name = 'myDB'
# DB_name = ':memory:'  # in-memory database


def connect(func):
    """Decorator to (re)open a sqlite database connection when needed.

    A database connection must be open when we want to perform a database query
    but we are in one of the following situations:
    1) there connection is None (no connection)
    2) the connection is closed
    We can understand in which scenario we are by executing a simple query in a
    try/except block. If the connection is None we will catch an AttributeError.
    If the connection is closed we will catch a sqlite3.ProgrammingError.

    Parameters
    ----------
    func : function
        function which performs the database query

    Returns
    -------
    inner func : function
    """
    def inner_func(*args, **kwargs):
        # First of all we need to find the connection object. It might be either
        # in args or kwargs.
        conns = list(filter(lambda x: type(x) is sqlite3.Connection, args))
        if conns:
            conn = conns[0]
        else:
            if 'conn' in kwargs.keys():
                conn = kwargs['conn']
            else:
                conn = None
        try:
            # I don't know if this is the simplest and fastest query to try
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError) as e:
            kwargs['conn'] = connect_to_db(DB_name)
        return func(*args, **kwargs)
    return inner_func


def tuple_to_dict(mytuple):
    mydict = dict()
    mydict['id'] = mytuple[0]
    mydict['name'] = mytuple[1]
    mydict['price'] = mytuple[2]
    mydict['quantity'] = mytuple[3]
    return mydict


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())


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
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection


def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()


@connect
def create_table(table_name, conn=None):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'name TEXT UNIQUE, price REAL, quantity INTEGER)'.format(table_name)
    c = conn.cursor()
    try:
        c.execute(sql)
        conn.commit()  # is it really needed?
    except OperationalError as e:
        print(e)


@connect
def insert_one(name, price, quantity, table_name, conn=None):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('name', 'price', 'quantity') VALUES (?, ?, ?)"\
        .format(table_name)
    c = conn.cursor()
    try:
        c.execute(sql, (name, price, quantity))
        conn.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '{}: "{}" already stored in table "{}"'.format(e, name, table_name))


@connect
def insert_many(items, table_name, conn=None):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('name', 'price', 'quantity') VALUES (?, ?, ?)"\
        .format(table_name)
    c = conn.cursor()
    entries = list()
    for x in items:
        entries.append((x['name'], x['price'], x['quantity']))
    try:
        c.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [x['name'] for x in items], table_name))


@connect
def select_one(item_name, table_name, conn=None):
    table_name = scrub(table_name)
    item_name = scrub(item_name)
    sql = 'SELECT * FROM {} WHERE name="{}"'.format(table_name, item_name)
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict(result)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(item_name, table_name))


@connect
def select_all(table_name, conn=None):
    table_name = scrub(table_name)
    sql = 'SELECT * FROM {}'.format(table_name)
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    return list(map(lambda x: tuple_to_dict(x), results))


@connect
def update_one(name, price, quantity, table_name, conn=None):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1)'\
        .format(table_name)
    sql_update = 'UPDATE {} SET price=?, quantity=? WHERE name=?'\
        .format(table_name)
    c = conn.cursor()
    c.execute(sql_check, (name,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_update, (price, quantity, name))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'
            .format(name, table_name))


@connect
def delete_one(name, table_name, conn=None):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1)'\
        .format(table_name)
    table_name = scrub(table_name)
    sql_delete = 'DELETE FROM {} WHERE name=?'.format(table_name)
    c = conn.cursor()
    c.execute(sql_check, (name,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_delete, (name,))  # we need the comma
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'
            .format(name, table_name))


def main():

    conn = connect_to_db()

    table_name = 'items'
    create_table(table_name, conn=conn)

    # CREATE
    insert_many(mock.items(), table_name='items', conn=conn)
    insert_one('beer', price=2.0, quantity=5, table_name='items', conn=conn)
    # if we try to insert an object already stored we get an ItemAlreadyStored
    # exception
    # insert_one('milk', price=1.0, quantity=3, table_name='items', conn=conn)

    # READ
    print('SELECT milk')
    print(select_one('milk', table_name='items', conn=conn))
    print('SELECT all')
    print(select_all(table_name='items', conn=conn))
    # if we try to select an object not stored we get an ItemNotStored exception
    # print(select_one('pizza', table_name='items', conn=conn))

    # UPDATE
    print('UPDATE bread, SELECT bread')
    update_one('bread', price=1.5, quantity=5, table_name='items', conn=conn)
    print(select_one('bread', table_name='items', conn=conn))
    # if we try to update an object not stored we get an ItemNotStored exception
    # print('UPDATE pizza')
    # update_one('pizza', price=1.5, quantity=5, table_name='items', conn=conn)

    # DELETE
    print('DELETE beer, SELECT all')
    delete_one('beer', table_name='items', conn=conn)
    print(select_all(table_name='items', conn=conn))
    # if we try to delete an object not stored we get an ItemNotStored exception
    # print('DELETE fish')
    # delete_one('fish', table_name='items', conn=conn)

    # save (commit) the changes
    # conn.commit()

    # close connection
    conn.close()

if __name__ == '__main__':
    main()
