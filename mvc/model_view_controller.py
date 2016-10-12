"""Model–view–controller (MVC) is a software architectural pattern.
MVC divides a given software application into three interconnected parts, so as
to separate internal representations of information (Model) from the ways that
information is presented to (View) or accepted from (Controller) the user.
"""
import basic_backend
import sqlite_backend
import dataset_backend
import mvc_exceptions as mvc_exc
import mvc_mock_objects as mock


class Model(object):
    """The Model class is the business logic of the application.

    The Model class provides methods to access the data of the application and
    performs CRUD operations. The data can be stored in the Model itself or in a
    database. Only the Model can access the database. A Model never calls View's
    methods.
    """
    def __init__(self):
        self._item_type = 'product'

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(self, name, price, quantity):
        raise NotImplementedError('Implement in subclass')

    def create_items(self, items):
        raise NotImplementedError('Implement in subclass')

    def read_item(self, name):
        raise NotImplementedError('Implement in subclass')

    def read_items(self):
        raise NotImplementedError('Implement in subclass')

    def update_item(self, name, price, quantity):
        raise NotImplementedError('Implement in subclass')

    def delete_item(self, name):
        raise NotImplementedError('Implement in subclass')


class ModelBasic(Model):

    def __init__(self, application_items):
        # super().__init__()  # ok in Python 3.x, not in 2.x
        super(self.__class__, self).__init__()  # also ok in Python 2.x
        self.create_items(application_items)

    def create_item(self, name, price, quantity):
        basic_backend.create_item(name, price, quantity)

    def create_items(self, items):
        basic_backend.create_items(items)

    def read_item(self, name):
        return basic_backend.read_item(name)

    def read_items(self):
        return basic_backend.read_items()

    def update_item(self, name, price, quantity):
        basic_backend.update_item(name, price, quantity)

    def delete_item(self, name):
        basic_backend.delete_item(name)


class ModelSQLite(Model):

    def __init__(self, application_items):
        # super().__init__()  # ok in Python 3.x, not in 2.x
        super(self.__class__, self).__init__()  # also ok in Python 2.x
        self._connection = sqlite_backend.connect_to_db(sqlite_backend.DB_name)
        sqlite_backend.create_table(self._item_type, self.connection)
        self.create_items(application_items)

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, new_connection):
        self._connection = new_connection

    def create_item(self, name, price, quantity):
        sqlite_backend.insert_one(
            name, price, quantity, table_name=self.item_type,
            conn=self.connection)

    def create_items(self, items):
        sqlite_backend.insert_many(
            items, table_name=self.item_type, conn=self.connection)

    def read_item(self, name):
        return sqlite_backend.select_one(
            name, table_name=self.item_type, conn=self.connection)

    def read_items(self):
        return sqlite_backend.select_all(
            table_name=self.item_type, conn=self.connection)

    def update_item(self, name, price, quantity):
        sqlite_backend.update_one(
            name, price, quantity, table_name=self.item_type,
            conn=self.connection)

    def delete_item(self, name):
        sqlite_backend.delete_one(
            name, table_name=self.item_type, conn=self.connection)


################################################################################
class ModelDataset(Model):

    def __init__(self, application_items):
        # super().__init__()  # ok in Python 3.x, not in 2.x
        super(self.__class__, self).__init__()  # also ok in Python 2.x
        dataset_backend.create_table(self._item_type)
        self.create_items(application_items)

    def create_item(self, name, price, quantity):
        dataset_backend.insert_one(
            name, price, quantity, table_name=self.item_type)

    def create_items(self, items):
        dataset_backend.insert_many(items, table_name=self.item_type)

    def read_item(self, name):
        return dataset_backend.select_one(name, table_name=self.item_type)

    def read_items(self):
        return dataset_backend.select_all(table_name=self.item_type)

    def update_item(self, name, price, quantity):
        dataset_backend.update_one(
            name, price, quantity, table_name=self.item_type)

    def delete_item(self, name):
        dataset_backend.delete_one(name, table_name=self.item_type)
################################################################################


class View(object):
    """The View class deals with how the data is presented to the user.

    A View should never call its own methods. Only a Controller should do it.
    """
    @staticmethod
    def show_bullet_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for item in items:
            print('* {}'.format(item))

    @staticmethod
    def show_number_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for i, item in enumerate(items):
            print('{}. {}'.format(i+1, item))

    @staticmethod
    def show_item(item_type, item, item_info):
        print('///////////////////////////////////////////////////////////////')
        print('Good news, we have some {}!'.format(item.upper()))
        print('{} INFO: {}'.format(item_type.upper(), item_info))
        print('///////////////////////////////////////////////////////////////')

    @staticmethod
    def display_missing_item_error(item, err):
        print('***************************************************************')
        print('We are sorry, we have no {}!'.format(item.upper()))
        print('{}'.format(err.args[0]))
        print('***************************************************************')

    @staticmethod
    def display_item_already_stored_error(item, item_type, err):
        print('***************************************************************')
        print('Hey! We already have {} in our {} list!'
              .format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('***************************************************************')

    @staticmethod
    def display_item_not_yet_stored_error(item, item_type, err):
        print('***************************************************************')
        print('We don\'t have any {} in our {} list. Please insert it first!'
              .format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('***************************************************************')

    @staticmethod
    def display_item_stored(item, item_type):
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Hooray! We have just added some {} to our {} list!'
              .format(item.upper(), item_type))
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    @staticmethod
    def display_change_item_type(older, newer):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---')
        print('Change item type from "{}" to "{}"'.format(older, newer))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---')

    @staticmethod
    def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---')
        print('Change {} price: {} --> {}'
              .format(item, o_price, n_price))
        print('Change {} quantity: {} --> {}'
              .format(item, o_quantity, n_quantity))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   ---')

    @staticmethod
    def display_item_deletion(name):
        print('---------------------------------------------------------------')
        print('We have just removed {} from our list'.format(name))
        print('---------------------------------------------------------------')


class Controller(object):
    """The Controller class associates the user input to a Model and a View.

    The Controller class handles the user's inputs, invokes Model's methods to
    alter the data, and calls specific View's methods to present the data back
    to the user. Model and View should be initialized by the Controller.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self, bullet_points=False):
        # items = self.model.get_items_generator()
        items = self.model.read_items()
        item_type = self.model.item_type
        if bullet_points:
            self.view.show_bullet_point_list(item_type, items)
        else:
            self.view.show_number_point_list(item_type, items)

    def show_item(self, item_name):
        try:
            item = self.model.read_item(item_name)
            item_type = self.model.item_type
            self.view.show_item(item_type, item_name, item)
        except mvc_exc.ItemNotStored as e:
            self.view.display_missing_item_error(item_name, e)

    def insert_item(self, name, price, quantity):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than or equal to 0'
        item_type = self.model.item_type
        try:
            self.model.create_item(name, price, quantity)
            self.view.display_item_stored(name, item_type)
        except mvc_exc.ItemAlreadyStored as e:
            self.view.display_item_already_stored_error(name, item_type, e)

    def update_item(self, name, price, quantity):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than or equal to 0'
        item_type = self.model.item_type

        try:
            older = self.model.read_item(name)
            self.model.update_item(name, price, quantity)
            self.view.display_item_updated(
                name, older['price'], older['quantity'], price, quantity)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(name, item_type, e)
            # if the item is not yet stored and we performed an update, we have
            # 2 options: do nothing or call insert_item to add it.
            # self.insert_item(name, price, quantity)

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        self.view.display_change_item_type(old_item_type, new_item_type)

    def delete_item(self, name):
        item_type = self.model.item_type
        try:
            self.model.delete_item(name)
            self.view.display_item_deletion(name)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(name, item_type, e)


if __name__ == '__main__':

    myitems = mock.items()

    # c = Controller(ModelBasic(myitems), View())
    # c = Controller(ModelSQLite(myitems), View())
    c = Controller(ModelDataset(myitems), View())

    c.show_items()
    c.show_items(bullet_points=True)
    c.show_item('chocolate')
    c.show_item('bread')

    c.insert_item('bread', price=1.0, quantity=5)
    c.insert_item('chocolate', price=2.0, quantity=10)
    c.show_item('chocolate')

    c.update_item('milk', price=1.2, quantity=20)
    c.update_item('ice cream', price=3.5, quantity=20)

    c.delete_item('fish')
    c.delete_item('bread')

    c.show_items()

    # we close the current sqlite database connection explicitly
    if type(c.model) is ModelSQLite:
        sqlite_backend.disconnect_from_db(
            sqlite_backend.DB_name, c.model.connection)
        # the sqlite backend understands that it needs to open a new connection
        c.show_items()
