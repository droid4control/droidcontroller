import unittest

from droidcontroller.cal.simpleevent import SimpleEvent

class SimpleEventTests(unittest.TestCase):
    '''
    This is the unittest for the droidcontroller.cal.simpleevent module
    '''
    def setUp(self):
        self.before = 50
        self.start = 100
        self.during1 = 110
        self.during2 = 190
        self.stop = 200
        self.after = 250
        self.data = "test"
        self.event = SimpleEvent(self.start, self.stop, self.data)

    def test_getters(self):
        self.assertEqual(self.start, self.event.get_start())
        self.assertEqual(self.stop, self.event.get_stop())
        self.assertEqual(self.data, self.event.get_data())

    def test_passed(self):
        self.assertFalse(self.event.is_passed(self.before))
        self.assertFalse(self.event.is_passed(self.during1))
        self.assertTrue(self.event.is_passed(self.after))

    def test_running(self):
        self.assertFalse(self.event.is_running(self.before))
        self.assertTrue(self.event.is_running(self.during1))
        self.assertFalse(self.event.is_running(self.after))

    def test_coming(self):
        self.assertTrue(self.event.is_coming(self.before))
        self.assertFalse(self.event.is_coming(self.during1))
        self.assertFalse(self.event.is_coming(self.after))

    def test_eq(self):
        self.assertEqual(self.event, self.event)
        self.assertEqual(self.event, SimpleEvent(self.start, self.stop, self.data))
        self.assertEqual(self.event, SimpleEvent(self.start, self.stop, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.before, self.start, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.before, self.during1, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.before, self.stop, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.before, self.after, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.start, self.during1, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.start, self.after, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.during1, self.during2, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.during1, self.stop, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.during1, self.after, 'x'))
        self.assertNotEqual(self.event, SimpleEvent(self.stop, self.after, 'x'))

    def test_lt(self):
        self.assertFalse(self.event < self.event)
        self.assertFalse(self.event < SimpleEvent(self.start, self.stop, self.data))
        self.assertFalse(self.event < SimpleEvent(self.start, self.stop, 'x'))
        self.assertFalse(self.event < SimpleEvent(self.before, self.start, 'x'))
        self.assertFalse(self.event < SimpleEvent(self.before, self.during1, 'x'))
        self.assertFalse(self.event < SimpleEvent(self.before, self.stop, 'x'))
        self.assertFalse(self.event < SimpleEvent(self.before, self.after, 'x'))
        self.assertTrue(self.event < SimpleEvent(self.start, self.during1, 'x'))
        self.assertFalse(self.event < SimpleEvent(self.start, self.after, 'x'))
        self.assertTrue(self.event < SimpleEvent(self.during1, self.during2, 'x'))
        self.assertTrue(self.event < SimpleEvent(self.during1, self.stop, 'x'))
        self.assertTrue(self.event < SimpleEvent(self.during1, self.after, 'x'))
        self.assertTrue(self.event < SimpleEvent(self.stop, self.after, 'x'))

    def test_value_error(self):
        self.assertRaises(TypeError, SimpleEvent, self.start, None, 'x')
        self.assertRaises(TypeError, SimpleEvent, None, self.stop, 'x')
        SimpleEvent(self.start, self.stop, None)
        self.assertRaises(ValueError, SimpleEvent, self.start, self.start, 'x')
        self.assertRaises(ValueError, SimpleEvent, self.start, self.before, 'x')
