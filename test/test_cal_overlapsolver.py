import unittest

from droidcontroller.cal.simpleevent import SimpleEvent
from droidcontroller.cal.overlapsolver import OverlapSolver

class OverlapSolverTests(unittest.TestCase):
    '''
    This is the unittest for the droidcontroller.cal.overlapsolver module
    '''
    def setUp(self):
        ''' Setup test case

                                  1    1    2    2
              time:     0    5    0    5    0    5
                        |....|....|....|....|....|
              events:    aaa   eee  iiii kk mmmmm
                          bbb ddddd hh   .. l n
                           ccc  ff  g  jjj     o
                        |....|....|....|....|....|
              result:   -abcccdeffd-ghijjkk-lmnom-
        '''

        self.events = (
                (1, 4, 'a'),
                (2, 5, 'b'),
                (3, 6, 'c'),
                (6, 11, 'd'),
                (7, 10, 'e'),
                (8, 10, 'f'),
                (12, 13, 'g'),
                (12, 14, 'h'),
                (12, 16, 'i'),
                (15, 18, 'j'),
                (17, 19, 'k'),
                (20, 21, 'l'),
                (20, 25, 'm'),
                (22, 23, 'n'),
                (23, 24, 'o'),
        )
        self.active_events = (
                None, 'a', 'b', 'c', 'c',   # 0 - 4
                'c', 'd', 'e', 'f', 'f',    # 5 - 9
                'd', None, 'g', 'h', 'i',   # 10 - 14
                'j', 'j', 'k', 'k', None,   # 15 - 19
                'l', 'm', 'n', 'o', 'm',    # 20 - 24
                None)                       # 25
        self.event_changes = (
                (1, 'a'),
                (2, 'b'),
                (3, 'c'),
                (6, 'd'),
                (7, 'e'),
                (8, 'f'),
                (10, 'd'),
                (11, None),
                (12, 'g'),
                (13, 'h'),
                (14, 'i'),
                (15, 'j'),
                (17, 'k'),
                (19, None),
                (20, 'l'),
                (21, 'm'),
                (22, 'n'),
                (23, 'o'),
                (24, 'm'),
                (25, None),
                (None, None)
                )
        self.solver = OverlapSolver()
        for event in self.events:
            self.solver.add_event(SimpleEvent(event[0], event[1], event[2]))

    def test_time_checks(self):
        events = []
        for ts in range(0, len(self.active_events)):
            event = self.solver.get_active(ts)
            if event:
                events.append(event.get_data())
            else:
                events.append(None)
        self.assertListEqual(list(self.active_events), events)
        self.assertEqual(len(self.solver._events), len(self.events))

    def test_time_checks_with_cleanup(self):
        events = []
        for ts in range(0, len(self.active_events)):
            self.solver.expire_passed_events(ts)
            event = self.solver.get_active(ts)
            if event:
                events.append(event.get_data())
            else:
                events.append(None)
        self.solver.expire_passed_events(len(self.active_events))
        self.assertEqual(len(self.solver._events), 0)

    def test_event_changes(self):
        change = 0
        ts = 0
        self.assertEqual(len(self.solver._events), len(self.events))
        while True:
            (ts, event) = self.solver.get_next_change(ts)
            self.assertEqual(ts, self.event_changes[change][0])
            if event:
                self.assertEqual(self.event_changes[change][1], event.get_data())
            else:
                self.assertIsNone(self.event_changes[change][1])
            change += 1
            if not ts:
                break
        self.assertEqual(len(self.solver._events), len(self.events))

    def test_event_changes_with_cleanup(self):
        self.assertEqual(len(self.solver._events), len(self.events))
        change = 0
        ts = 0
        while True:
            (ts, event) = self.solver.get_next_change(ts)
            self.assertEqual(ts, self.event_changes[change][0])
            if event:
                self.assertEqual(self.event_changes[change][1], event.get_data())
            else:
                self.assertIsNone(self.event_changes[change][1])
            change += 1
            if not ts:
                break
            self.solver.expire_passed_events(ts)
        self.assertEqual(len(self.solver._events), 0)
