from droidcontroller.cal.simpleevent import SimpleEvent

class OverlapSolver(object):
    '''
    If there are overlapping events, this class helps to find an
    active one. Only one event can be active in any given moment.

    If there are more than one event present at given time then
    following rules will determine which one should be used:

    - the event which started latter
    - if multiple events start at the same time, then event ending
      first will be choosed

    It is not allowed to fully overlap two (or more) events
    '''

    def __init__(self):
        ''' Initialize an instance of the OverlapSolver
        '''
        self._events = []

    def add_event(self, event):
        ''' Add one SimpleEvent to the OverlapSolver

        New event should have unique start and stop times. Otherwise
        ValueError will be raised.

        :param event: SimpleEvent instance
        '''
        if event in self._events:
            raise ValueError('similar event is already in eventlist')
        self._events.append(event)

    def del_event(self, event):
        ''' Delete given event from the OverlapSolver event list

        If no such event exists, then ValueError will be raised.

        :param event: SimpleEvent instance
        '''
        if event in self._events:
            self._events.remove(event)
        else:
            raise ValueError('no such event known')

    def get_active(self, ts):
        ''' Get active event

        If no event is active, then None will re returned

        :param ts: timestamp

        :returns: active event instance or None
        '''
        running = self._get_all_running_events(ts)
        if not running:
            return None
        return sorted(running, reverse=True)[0]

    def get_next_active(self, ts):
        ''' Get event which will be active next

        If there is no more events coming, then None will re returned

        :param ts: timestamp

        :returns: next active event instance or None
        '''
        coming = self._get_all_coming_events(ts)
        if not coming:
                return None
        return self.get_active(sorted(coming)[0].get_start())

    def get_next_change(self, ts):
        ''' Get time and event for next change

        This method returns time when active event stops or when a new
        overlapping event with higher priority kicks in.

        If there is no event active and no more events are coming,
        then (None, None) will be returned.

        If no more events are coming then stop time of active event
        and None will be returned.

        :param ts: timestamp

        :returns: duple of timestamp of change and next event instance
        '''
        active = self.get_active(ts)
        next_active = self.get_next_active(ts)
        if not next_active:
            if active:
                prev_active = self.get_active(active.get_stop())
                if prev_active:
                    return (active.get_stop(), prev_active)       # 1
                else:
                    return (active.get_stop(), None)              # 2
            else:
                return (None, None)                               # 3
        else:
            if not active:
                return (next_active.get_start(), next_active)     # 4
            else:
                if active.get_stop() < next_active.get_start():
                    prev_active = self.get_active(active.get_stop())
                    if prev_active:
                        return (active.get_stop(), prev_active)   # 5
                    else:
                        return (active.get_stop(), None)          # 6
                elif active.get_stop() == next_active.get_start():
                    return (next_active.get_start(), next_active) # 7
                else:
                    return (next_active.get_start(), next_active) # 8

    def get_active_new(self, ts):
        ''' Find an active event and create a new SimpleEvent instance
        with stop time based on next change (time when the active event
        stops or when a new overlapping event with higher priority
        kicks in).

        :param ts: timestamp

        :returns: a new active event instance or None
        '''
        active = self.get_active(ts)
        if not active:
            return None
        (next_change, next_event) = self.get_next_change(ts)
        return SimpleEvent(active.get_start(), next_change, active.get_data())

    def expire_passed_events(self,ts):
        ''' Expire events that are already passed

        Remove events, which are finished by given time, from the
        event list for a cleanup purposes. This saves memory and
        event list processing time.

        :param ts: timestamp
        '''
        freshevents = [e for e in self._events if not e.is_passed(ts)]
        self._events = freshevents

    def _get_all_running_events(self, ts):
        return [e for e in self._events if e.is_running(ts)]

    def _get_all_coming_events(self, ts):
        return [e for e in self._events if e.is_coming(ts)]
