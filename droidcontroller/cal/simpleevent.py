
class SimpleEvent(object):
    '''
    Base class for simple single event

    This event has only three attributes: start time, stop time and
    arbitary data (name, description or whatever)

    This class is intended for event lookup and comparision
    '''

    START = 0
    STOP = 1
    DATA = 2

    def __init__(self, start, stop, data):
        ''' Create new immutable event

        :param start: event start time
        :param stop: event stop time
        :param data: event name, description or other data
        '''
        if stop <= start:
            raise ValueError('event stop MUST BE after start')
        self._setup = (start, stop, data)

    def get_start(self):
        ''' Return the event start time

        :returns: The event start time
        '''
        return self._setup[self.START]

    def get_stop(self):
        ''' Return the event stop time

        :returns: The event stop time
        '''
        return self._setup[self.STOP]

    def get_data(self):
        ''' Return the event data

        :returns: The event data
        '''
        return self._setup[self.DATA]

    def is_passed(self, ts):
        ''' Check if event is passed

        :param ts: current timestamp

        :returns: True, if event is already passed
        '''
        return ts >= self.get_stop()

    def is_running(self, ts):
        ''' Check if event is running

        :param ts: current timestamp

        :returns: True, if event is running
        '''
        return ts >= self.get_start() and ts < self.get_stop()

    def is_coming(self, ts):
        ''' Check if event is in the future

        :param ts: current timestamp

        :returns: True, if event is coming in the future
        '''
        return ts < self.get_start()

    def __eq__(self, other):
        ''' Check if event is equal with other event

        Events are considered equal if they fully overlap i.e.
        their start and stop times are equal.
        '''

        return self.get_start() == other.get_start() and \
               self.get_stop() == other.get_stop()

    def __lt__(self, other):
        ''' Check if event happens before other event

        This is used for sorting where events will be ordered
        based on start time. In case of equal start time,
        the longest event will be first.
        '''
        if self.get_start() < other.get_start():
            return True
        elif self.get_start() == other.get_start() and \
             self.get_stop() > other.get_stop():
            return True
        else:
            return False

    def __str__(self):
        return '%d-%d: %s' % (self.get_start(), self.get_stop(), \
                str(self.get_data()))
