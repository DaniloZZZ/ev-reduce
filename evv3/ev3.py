from itertools import chain

class SyncModel:
    """
    This model is the very basic implemetation of ev-reduce api.
    The event generators are merged into a single generator
    and for every event a corresponding reducer is called.

    Everything is going on in a single thread
    """
    def __init__(self):
        self.sources = []
        self.reducers = {}
        self.actors = []
        self.data = {}

    def add_source(self, src):
        """ Add a generator of events

        :param src: a generator that yields an Event
        :type src: generator
        """
        self.sources.append(src)

    def add_actor(self,act):
        """ Add an actor that will be called after every
        reducer rerturns an action

        :param act: a callable that takes Action and returns None if\
                the action succeded. Otherviwse an ev-red.Error event \
                will be fired with data returned
        :type act: callable
        """
        self.actors.append(act)

    def add_reducer(self, reducer , subscribe=[]):
        """ Add a reducer that subscribes to events

        :param reducer: a callable that takes event and data\
        and returns action and modified data.
        :type reducer: callable

        :param subscribe: list of tokens that specify type of event\
                to which the reducer will be called
        :type subscribe: list

        """
        for t in subscribe:
            self.reducers.setdefault(t,[])
            self.reducers[t].append(reducer)

    def start(self):
        """
        Start execution
        """
        gen = chain(*self.sources)
        for ev in gen:
            t =  ev[0]
            reds = self.reducers.get(t,[])
            for r in reds:
                result = r(ev, self.data)
                if result is None:
                    continue
                else:
                    act,data = result
                self.data.update(data)
                self._dispatch(act)

    def _dispatch(self,act):
        for a in self.actors:
            result = a(act)
            if result is not None:
                print("evv3: action returned an error", result)

