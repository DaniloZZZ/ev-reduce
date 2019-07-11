import multiprocessing as mpc
from threading import Thread
from itertools import chain


def _pipe_reader(pipe_end):
    while True:
        yield pipe_end.recv()

class MprocModel:
    """
    Sources and actions go in main process, but in different threads.

    Reducers go in other process.

    Communication is performed with two pipes: source-reducer and reducer-sourcce
    """
    def __init__(self):
        self.sources = []
        self.reducers = {}
        self.actors = {}
        self.data = {}
        self.to_reducers, self.from_source = mpc.Pipe()
        self.from_reducers, self.to_actions = mpc.Pipe()

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
            print("decor", func)
            self.add_reducer(func, subscribe=subscribe)
        return decor

    def start(self):
        """
        Start execution
        """
        def reducers_loop():
            gen = _pipe_reader(self.from_source)
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
        p = mpc.Process(
            target=reducers_loop,
            args=(),
        )
        p.start()

        gen_src = chain(*self.sources)
        def emitter_loop():
            for ev in gen_src:
                self._emit(ev)

        emitter = Thread( 
            target=emitter_loop
        )
        emitter.start()

        while True:
            act = self.from_reducers.recv()
            self._exec_act(act)

        p.terminate()
        p.join()
        emitter.join()

    def _emit(self,ev):
        self.to_reducers.send(ev)

    def _exec_act(self,act):
        label = act[0]
        action = self.actors.get(label)
        if action is None:
            print("Unknown label occured")
        else:
            result = action(act)
            if result is not None:
                print("evv3: action returned an error", result)

    def _dispatch(self,act):
        self.to_actions.send(act)
