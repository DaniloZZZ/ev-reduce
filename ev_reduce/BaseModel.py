from  .helpers.logging import log

class BaseModel:
    def __init__(self):
        self.sources = []
        self.reducers = {}
        self.actors = {}
        self.data = {}
        self.logger = log.getLogger('base')

        self.add_reducer(
            lambda *x: (('_STOP',''),{})
            ,subscribe=['_stop']
        )
        self.add_actor( '_STOP', lambda *x: '_cmd_stop')

    def add_source(self, src):
        """ Add a generator of events

        :param src: a generator that yields an Event
        :type src: generator
        """
        self.sources.append(src)

    def source(self, gen):
        """Decorator for adding a source to model"""
        def start(*args, **kwargs):
            src = gen(*args, **kwargs)
            self.add_source(src)
        return start

    def add_actor(self, label, act):
        """ Add an actor that will be called after every
        reducer rerturns an action

	:param label: A label that reducer return
	:type label: str

        :param act: a callable that takes Action and returns None if\
                the action succeded. Otherviwse an ev-red.Error event \
                will be fired with data returned
        :type act: callable

        """
        self.actors[label] = act

    # for decorator use
    def actor(self, label):
        def decor(func):
            self.add_actor(label, func)
        return decor

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

    def reducer(self, subscribe=[]):
        def decor(func):
            self.add_reducer(func, subscribe=subscribe)
        return decor

    def _emit(self,ev):
        log.debug(f"Emitting event: {ev}")
        self.to_reducers.send(ev)
    def _dispatch(self,act):
        log.debug(f"Dispatching action: {act}")
        self.to_actions.send(act)

    def _handle_ev(self, ev):
        log.debug(f"New event: {ev}")
        t =  ev[0]
        reds = self.reducers.get(t,[])
        for r in reds:
            result = r(ev, self.data)
            if result is None:
                continue
            else:
                act,data = result
                self.data.update(data)
                yield act


    def _exec_act(self,act):
        log.debug(f"Executing action: {act}")
        label = act[0]
        action = self.actors.get(label)
        if action is None:
            log.warn(f"Unknown label occured: {label}")
        else:
            result = action(act)
            if result=='_cmd_stop':
                log.info("Got stop signal, returning")
                return result
            if result is not None:
                log.error(f"Action returned an error {result}")
                return result

