import unittest
import sys
from io import StringIO
from ddt import ddt, data
from contextlib import contextmanager
from borg import Borg, ChildShare, ChildNotShare
from interpreter import Interpreter, DeviceNotAvailable, ActionNotAvailable,\
    IncorrectAction
from factory_method import factory_method
from abstract_factory import TriangleFactory, QuadrilateralFactory, \
    give_me_some_polygons
from memento import Originator
from null_object import NullObject
from observer import Publisher, Subscriber
from proxy import Proxy, Implementation
from singleton import Singleton, Child, GrandChild
from strategy import Strategy, execute_replacement1, execute_replacement2


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestBorg(unittest.TestCase):

    def test_two_borgs_have_different_identity(self):
        a = Borg('Mark')
        b = Borg('Luke')
        self.assertIsNot(a, b)

    def test_two_borgs_share_common_state(self):
        a = Borg('Mark')
        b = Borg('Luke')
        self.assertEqual(a.state, b.state)

    def test_borg_and_childshare_share_common_state(self):
        a = Borg('Mark')
        c = ChildShare('Paul', color='red')
        self.assertEqual(a.state, c.state)

    def test_borg_and_childnotshare_do_not_share_common_state(self):
        a = Borg('Mark')
        d = ChildNotShare('Andrew', age=5)
        self.assertNotEqual(a.state, d.state)

    def test_two_childnotshare_share_common_state(self):
        d = ChildNotShare('Andrew', age=5)
        e = ChildNotShare('Tom', age=7)
        self.assertEqual(d.state, e.state)

    def test_update_state(self):
        a = Borg('Mark')
        c = ChildShare('Paul', color='red')
        self.assertIn('color', a.state)
        d = ChildNotShare('Andrew', age=5)
        a.name = 'James'
        self.assertEqual(a.name, c.name)
        self.assertNotEqual(a.name, d.name)


@ddt
class TestInterpreter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.interpreter = Interpreter()

    def test_opening_the_garage(self):
        with captured_output() as (out, err):
            self.interpreter.interpret('open -> garage')
        output = out.getvalue().strip()
        self.assertEqual(output, 'opening the garage')

    def test_heat_the_boiler_up(self):
        with captured_output() as (out, err):
            self.interpreter.interpret('heat -> boiler -> 5')
        output = out.getvalue().strip()
        self.assertEqual(output, 'heat the boiler up by 5 degrees')

    def test_cool_the_boiler_down(self):
        with captured_output() as (out, err):
            self.interpreter.interpret('cool -> boiler -> 3')
        output = out.getvalue().strip()
        self.assertEqual(output, 'cool the boiler down by 3 degrees')

    def test_switch_the_television_on(self):
        with captured_output() as (out, err):
            self.interpreter.interpret('switch on -> television')
        output = out.getvalue().strip()
        self.assertEqual(output, 'switch on the television')

    def test_switch_the_television_off(self):
        with captured_output() as (out, err):
            self.interpreter.interpret('switch off -> television')
        output = out.getvalue().strip()
        self.assertEqual(output, 'switch off the television')

    @data('cool -> boiler', 'switch off -> television -> 4')
    def test_raise_incorrect_action(self, val):
        self.assertRaises(IncorrectAction, self.interpreter.interpret, val)

    @data('break -> garage', 'smash -> television')
    def test_raise_action_not_available(self, val):
        self.assertRaises(ActionNotAvailable, self.interpreter.interpret, val)

    @data('read -> book', 'open -> gate')
    def test_raise_device_not_available(self, val):
        self.assertRaises(DeviceNotAvailable, self.interpreter.interpret, val)


class TestMemento(unittest.TestCase):

    def test_restore_state(self):
        originator = Originator()
        originator.state = 'State1'
        memento1 = originator.save()
        originator.state = 'State2'
        originator.restore(memento1)
        self.assertEqual(originator.state, 'State1')


class TestNullObject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.null = NullObject(name='Bob')

    def test_null_object_is_null(self):
        self.assertTrue(self.null.is_null)

    def test_null_has_no_name(self):
        self.assertIsNot(self.null.name, 'Bob')

    def test_repr_of_null_object(self):
        self.assertEqual(repr(self.null), '<Null>')

    def test_do_stuff_does_nothing(self):
        self.assertIsNone(self.null.do_stuff())

    def test_get_stuff_gets_nothing(self):
        self.assertIsNone(self.null.get_stuff())


class TestFactoryMethod(unittest.TestCase):

    def test_factory_cannot_manufacture_a_train(self):
        self.assertRaises(ValueError, factory_method, 'train')


class TestAbstractFactory(unittest.TestCase):

    def test_factories_are_abstract_and_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            TriangleFactory()
        with self.assertRaises(TypeError):
            QuadrilateralFactory()

    def test_triangle_factory_produces_triangles(self):
        triangle = TriangleFactory.make_polygon()
        self.assertIn(triangle.__class__.__name__, TriangleFactory.products())

    def test_polygons_produced_are_subset_of_all_available_polygons(self):
        all_available_polygons = set(TriangleFactory.products())\
            .union(QuadrilateralFactory.products())
        polygons = give_me_some_polygons(
            [TriangleFactory, QuadrilateralFactory])
        polygons_produced = set([p.__class__.__name__ for p in polygons])
        self.assertTrue(polygons_produced.issubset(all_available_polygons))


class TestObserver(unittest.TestCase):

    def setUp(self):
        self.newsletters = ['Tech', 'Travel', 'Fashion']
        self.pub = Publisher(self.newsletters)
        subscribers = [('s0', 'Tom'), ('s1', 'Sara')]
        for sub, name in subscribers:
            setattr(self, sub, Subscriber(name))

        # before each test case, set some subscriptions
        self.pub.register('Tech', self.s0)
        self.pub.register('Travel', self.s0)
        self.pub.register('Travel', self.s1)

    def tearDown(self):
        # after each test case, reset the subscriptions
        for newsletter in self.newsletters:
            if self.s0 in self.pub.subscriptions[newsletter]:
                self.pub.unregister(newsletter, self.s0)
            if self.s1 in self.pub.subscriptions[newsletter]:
                self.pub.unregister(newsletter, self.s1)

    def test_register_subscriber(self):
        john = Subscriber('John')
        self.pub.register(newsletter='Tech', who=john)
        self.assertEqual(self.pub.subscriptions['Tech'][john], john.receive)
        self.pub.unregister(newsletter='Tech', who=john)  # cleanup

    def test_unregister_subscriber(self):
        self.assertIn(self.s0, self.pub.get_subscriptions('Tech'))
        self.pub.unregister('Tech', self.s0)
        self.assertNotIn(self.s0, self.pub.get_subscriptions('Tech'))

    def test_dispatch_newsletter(self):
        with captured_output() as (out, err):
            self.pub.dispatch(
                newsletter='Tech', message='Tech Newsletter num 1')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Tom received: Tech Newsletter num 1')

    def test_get_subscription_without_subscribers(self):
        self.assertEqual(self.pub.get_subscriptions('Fashion'), {})

    def test_get_subscription_with_subscribers(self):
        self.assertIn(self.s0, self.pub.get_subscriptions('Tech'))

    def test_add_newsletter(self):
        self.assertNotIn('Videogames', self.pub.subscriptions.keys())
        self.pub.add_newsletter('Videogames')
        self.assertIn('Videogames', self.pub.subscriptions.keys())

    def test_subscription_does_not_exist(self):
        with self.assertRaises(KeyError):
            self.pub.subscriptions['Videogames']


class TestProxy(unittest.TestCase):

    def test_load_real_or_cached_object(self):
        p1 = Proxy(Implementation('RealObject1'))

        # the first time we call do_stuff we need to load the real object
        with captured_output() as (out, err):
            p1.do_stuff()
        output = out.getvalue().strip()
        self.assertEqual(output, 'load RealObject1\ndo stuff on RealObject1')

        # after that, loading is unnecessary (we use the cached object)
        with captured_output() as (out, err):
            p1.do_stuff()
        output = out.getvalue().strip()
        self.assertEqual(output, 'do stuff on RealObject1')


class TestSingleton(unittest.TestCase):

    def test_two_singletons_have_same_identity(self):
        s1 = Singleton('Sam')
        s2 = Singleton('Tom')
        self.assertIs(s1, s2)

    def test_singleton_and_child_have_different_identity(self):
        s1 = Singleton('Sam')
        c1 = Child('John')
        self.assertIsNot(s1, c1)

    def test_two_children_have_same_identity(self):
        c1 = Child('John')
        c2 = Child('Andy')
        self.assertIs(c1, c2)

    def test_child_and_grandchild_have_different_identity(self):
        c1 = Child('John')
        g1 = GrandChild('Bob')
        self.assertIsNot(c1, g1)


class TestStrategy(unittest.TestCase):

    def test_default_strategy(self):
        self.assertEqual(Strategy().name, 'Strategy_default')

    def test_replacement_strategy_one(self):
        self.assertEqual(Strategy(execute_replacement1).name,
                         'Strategy_execute_replacement1')

    def test_replacement_strategy_two(self):
        self.assertEqual(Strategy(execute_replacement2).name,
                         'Strategy_execute_replacement2')


if __name__ == '__main__':
    unittest.main()
