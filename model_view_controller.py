"""Model–view–controller (MVC) is a software architectural pattern.
MVC divides a given software application into three interconnected parts, so as
to separate internal representations of information (Model) from the ways that
information is presented to (View) or accepted from (Controller) the user.
"""


class ItemAlreadyStored(Exception):
    pass


class ItemNotStored(Exception):
    pass


class Model(object):
    """The Model class is the business logic of the application.

    The Model class provides methods to access the data of the application and
    performs CRUD operations. The data can be stored in the Model itself or in a
    database. Only the Model can access the database. A Model never calls View's
    methods.
    """
    def __init__(self):
        self._item_type = 'product'
        self._items = {
            'milk': {'price': 1.50, 'quantity': 10},
            'eggs': {'price': 0.20, 'quantity': 100},
            'cheese': {'price': 2.00, 'quantity': 10}
        }

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def get_items_generator(self):
        for item in self._items:
            yield item

    def get_items_list(self):
        return [item for item in self._items]

    def get(self, item):
        myitem = self._items.get(item, None)
        if myitem is None:
            raise ItemNotStored('The {0} "{1}" is not stored in the {0} list'
                                .format(self.item_type, item))
        else:
            return myitem

    def insert_item(self, item, price, quantity):
        myitem = self._items.get(item, None)
        if myitem is None:
            self._items[item] = {'price': price, 'quantity': quantity}
        else:
            raise ItemAlreadyStored('The {0} "{1}" is already in the {0} list.'
                                    .format(self.item_type, item))

    def update_item(self, item, price, quantity):
        myitem = self._items.get(item, None)
        if myitem is None:
            raise ItemNotStored('The {0} "{1}" is not stored in the {0} list'
                                .format(self.item_type, item))
        else:
            self._items[item] = {'price': price, 'quantity': quantity}


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
        items = self.model.get_items_list()
        item_type = self.model.item_type
        if bullet_points:
            self.view.show_bullet_point_list(item_type, items)
        else:
            self.view.show_number_point_list(item_type, items)

    def show_item(self, item):
        try:
            item_info = self.model.get(item)
            item_type = self.model.item_type
            self.view.show_item(item_type, item, item_info)
        except ItemNotStored as e:
            self.view.display_missing_item_error(item, e)

    def insert_item(self, item, price, quantity):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than or equal to 0'
        item_type = self.model.item_type
        try:
            self.model.insert_item(item, price, quantity)
            self.view.display_item_stored(item, item_type)
            self.show_items()
        except ItemAlreadyStored as e:
            self.view.display_item_already_stored_error(item, item_type, e)

    def update_item(self, item, price, quantity):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than or equal to 0'
        item_type = self.model.item_type

        try:
            older = self.model.get('milk')
            self.model.update_item(item, price, quantity)
            self.view.display_item_updated(
                item, older['price'], older['quantity'], price, quantity)
        except ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(item, item_type, e)

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        self.view.display_change_item_type(old_item_type, new_item_type)


if __name__ == '__main__':
    c = Controller(Model(), View())

    c.show_items()
    c.show_items(bullet_points=True)

    c.show_item('milk')
    c.insert_item('milk', price=1.0, quantity=5)

    c.show_item('chocolate')
    c.insert_item('chocolate', price=2.0, quantity=10)
    c.show_item('chocolate')

    c.update_item_type('food')
    c.show_items()

    c.update_item('ice cream', price=3.5, quantity=20)
    c.update_item('milk', price=1.2, quantity=20)
    c.show_item('milk')
