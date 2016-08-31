"""Model–view–controller (MVC) is a software architectural pattern.
MVC divides a given software application into three interconnected parts, so as
to separate internal representations of information (Model) from the ways that
information is presented to (View) or accepted from (Controller) the user.
"""


class MissingItemException(Exception):
    pass


class ItemAlreadyStored(Exception):
    pass


class Model(object):
    """Model fetches the data to be presented from persistent storage.
    It's the business logic of the application.
    Model is also responsible for working with the databases and performing
    operations like Insertion, Update and Deletion.
    Every model is meant to provide a certain kind of data to the controller,
    when invoked.

    """
    items = {
        'milk': {'price': 1.50, 'quantity': 10},
        'eggs': {'price': 0.20, 'quantity': 100},
        'cheese': {'price': 2.00, 'quantity': 10}
    }

    item_type = 'product'

    def get_items_generator(self):
        for item in self.items:
            yield item

    def get_items_list(self):
        return [item for item in self.items]

    def get(self, item):
        myitem = self.items.get(item, None)
        if myitem is None:
            raise MissingItemException(
                'The {} "{}" is missing.'.format(self.item_type, item))
        else:
            return myitem

    def insert_item(self, item):
        myitem = self.items.get(item, None)
        if myitem is None:
            # TODO: price and quantity must be set by the user
            # TODO: if price and/or quantity are missing or wrong, we have to
            # raise an exception
            self.items[item] = {'price': 1.00, 'quantity': 1}
        else:
            raise ItemAlreadyStored('The {0} "{1}" is already in the {0} list.'
                                    .format(self.item_type, item))


class View(object):
    """View deals with how the fetched data is presented to the user.
    Select a template to display the results to the user's requests.
    View, also referred as presentation layer, is responsible for displaying the
    results obtained by the controller from the model component.

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


class Controller(object):
    """Controller associates the user input to a Model and a View.
    Controls user input and response back to the user.
    Invokes a Model for the requested user inputs.
    It's a middle man between user, business logic (Model) and formatting (View)
    It's the entry point for all user's requests and inputs.
    The controller accepts the user inputs, parses them and decides which type
    of Model and View should be invoked.

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
        except MissingItemException as e:
            self.view.display_missing_item_error(item, e)

    def insert_item(self, item):
        item_type = self.model.item_type
        try:
            self.model.insert_item(item)
            self.view.display_item_stored(item, item_type)
            self.show_items()
        except ItemAlreadyStored as e:
            self.view.display_item_already_stored_error(item, item_type, e)
        # TODO: exceptions to handle the cases where the item could be stored,
        # but quantity/price are wrong.

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        self.view.display_change_item_type(old_item_type, new_item_type)


if __name__ == '__main__':
    m = Model()
    v = View()
    c = Controller(m, v)

    c.show_items()
    c.show_items(bullet_points=True)

    c.show_item('milk')
    c.insert_item('milk')

    c.show_item('chocolate')
    c.insert_item('chocolate')
    c.show_item('chocolate')

    c.update_item_type('food')
    c.show_items()
    c.show_item('milk')
    # c.update_quantity()
    # c.update_price()
