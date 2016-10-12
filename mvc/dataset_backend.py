"""Some tests with the dataset module.

https://dataset.readthedocs.io/en/latest/
"""
import dataset
from sqlalchemy.exc import IntegrityError, NoSuchTableError
import mvc_exceptions as mvc_exc
import mvc_mock_objects as mock


DB_name = 'myDB'


class UnsupportedDatabaseEngine(Exception):
    pass


def connect(func):
    """Decorator to (re)open a database connection when needed.

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
        conns = list(filter(lambda x: type(x) is dataset.Database, args))
        if not conns and not 'conn' in kwargs.keys():
            connect_to_db(DB_name)
        return func(*args, **kwargs)
    return inner_func


def connect_to_db(db_name=None, db_engine='sqlite'):
    """Connect to a database. Create the database if there isn't one yet.

    The database can be a SQLite DB (either a DB file or an in-memory DB), or a
    PostgreSQL DB. In order to connect to a PostgreSQL DB you have first to
    create a database, create a user, and finally grant him all necessary
    privileges on that database and tables.
    'postgresql://<username>:<password>@localhost:<PostgreSQL port>/<db name>'
    Note: at the moment it looks it's not possible to close a connection
    manually (e.g. like calling conn.close() in sqlite3).


    Parameters
    ----------
    db_name : str or None
        database name (without file extension .db)
    db_engine : str
        database engine ('sqlite' or 'postgres')

    Returns
    -------
    dataset.persistence.database.Database
        connection to a database
    """
    engines = {'sqlite', 'postgres'}
    if db_name is None:
        db_string = 'sqlite:///:memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        if db_engine == 'sqlite':
            db_string = 'sqlite:///{}.db'.format(DB_name)
            print('New connection to SQLite DB...')
        elif db_engine == 'postgres':
            db_string = \
                'postgresql://test_user:test_password@localhost:5432/testdb'
            # db_string = \
            #     'postgresql://test_user2:test_password2@localhost:5432/testdb'
            print('New connection to PostgreSQL DB...')
        else:
            raise UnsupportedDatabaseEngine(
                'No database engine with this name. '
                'Choose one of the following: {}'.format(engines))

    return dataset.connect(db_string)


@connect
def create_table(table_name, conn=None):
    """Load a table or create it if it doesn't exist yet.

    The function load_table can only load a table if exist, and raises a
    NoSuchTableError if the table does not already exist in the database.

    The function get_table either loads a table or creates it if it doesn't
    exist yet. The new table will automatically have an id column unless
    specified via optional parameter primary_id, which will be used as the
    primary key of the table.

    Parameters
    ----------
    table_name : str
    conn : dataset.persistence.database.Database
    """
    try:
        conn.load_table(table_name)
    except NoSuchTableError as e:
        print('Table {} does not exist. It will be created now'.format(e))
        conn.get_table(table_name, primary_id='name', primary_type='String')
        print('Created table {} on database {}'.format(table_name, DB_name))


@connect
def insert_one(name, price, quantity, table_name, conn=None):
    """Insert a single item in a table.

    Parameters
    ----------
    name : str
    price : float
    quantity : int
    table_name : dataset.persistence.table.Table
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemAlreadyStored: if the record is already stored in the table.
    """
    table = conn.load_table(table_name)
    try:
        table.insert(dict(name=name, price=price, quantity=quantity))
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '"{}" already stored in table "{}".\nOriginal Exception raised: {}'
            .format(name, table.table.name, e))


@connect
def insert_many(items, table_name, conn=None):
    """Insert all items in a table.

    Parameters
    ----------
    items : list
        list of dictionaries
    table_name : str
    conn : dataset.persistence.database.Database
    """
    # TODO: check what happens if 1+ records can be inserted but 1 fails
    table = conn.load_table(table_name)
    try:
        for x in items:
            table.insert(dict(
                name=x['name'], price=x['price'], quantity=x['quantity']))
    except IntegrityError as e:
        print('At least one in {} was already stored in table "{}".\nOriginal '
              'Exception raised: {}'
              .format([x['name'] for x in items], table.table.name, e))


@connect
def select_one(name, table_name, conn=None):
    """Select a single item in a table.

    The dataset library returns a result as an OrderedDict.

    Parameters
    ----------
    name : str
        name of the record to look for in the table
    table_name : str
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        return dict(row)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(name, table.table.name))


@connect
def select_all(table_name, conn=None):
    """Select all items in a table.

    The dataset library returns results as OrderedDicts.

    Parameters
    ----------
    table_name : str
    conn : dataset.persistence.database.Database

    Returns
    -------
    list
        list of dictionaries. Each dict is a record.
    """
    table = conn.load_table(table_name)
    rows = table.all()
    return list(map(lambda x: dict(x), rows))


@connect
def update_one(name, price, quantity, table_name, conn=None):
    """Update a single item in the table.

    Note: dataset update method is a bit counterintuitive to use. Read the docs
    here: https://dataset.readthedocs.io/en/latest/quickstart.html#storing-data
    Dataset has also an upsert functionality: if rows with matching keys exist
    they will be updated, otherwise a new row is inserted in the table.

    Parameters
    ----------
    name : str
    price : float
    quantity : int
    table_name : str
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        item = {'name': name, 'price': price, 'quantity': quantity}
        table.update(item, keys=['name'])
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'
            .format(name, table.table.name))


@connect
def delete_one(item_name, table_name, conn=None):
    """Delete a single item in a table.

    Parameters
    ----------
    item_name : str
    table_name : str
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=item_name)
    if row is not None:
        table.delete(name=item_name)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'
            .format(item_name, table.table.name))


def main():

    conn = connect_to_db()

    table_name = 'items'
    create_table(table_name, conn=conn)

    # CREATE
    insert_many(items=mock.items(), table_name=table_name, conn=conn)
    insert_one('beer', price=2.0, quantity=5, table_name=table_name, conn=conn)
    # if we try to insert an object already stored we get an ItemAlreadyStored
    # exception
    # insert_one('beer', 2.0, 5, table_name=table_name, conn=conn)

    # READ
    print('SELECT milk')
    print(select_one('milk', table_name=table_name, conn=conn))
    print('SELECT all')
    print(select_all(table_name=table_name, conn=conn))
    # if we try to select an object not stored we get an ItemNotStored exception
    # print(select_one('pizza', table_name=table_name, conn=conn))

    # UPDATE
    print('UPDATE bread, SELECT bread')
    update_one('bread', price=1.5, quantity=5, table_name=table_name, conn=conn)
    print(select_one('bread', table_name=table_name, conn=conn))
    # if we try to update an object not stored we get an ItemNotStored exception
    # print('UPDATE pizza')
    # update_one('pizza', 9.5, 5, table_name=table_name, conn=conn)

    # DELETE
    print('DELETE beer, SELECT all')
    delete_one('beer', table_name=table_name, conn=conn)
    print(select_all(table_name=table_name, conn=conn))
    # if we try to delete an object not stored we get an ItemNotStored exception
    # print('DELETE fish')
    # delete_one('fish', table_name=table_name, conn=conn)

if __name__ == '__main__':
    main()
