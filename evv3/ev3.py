from itertools import chain

class EvV3:
    def __init__(self):
        self.sources = []
        self.reducers = {}
        self.actors = []
        self.data = {}

    def add_source(self, src):
        self.sources.append(src)
    def add_actor(self,act):
        self.actors.append(act)

    def add_reducer(self, red , subscribe=[]):
        for t in subscribe:
            self.reducers.setdefault(t,[])
            self.reducers[t].append(red)

    def start(self):
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

