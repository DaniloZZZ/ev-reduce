
class listAPI:
    def __init__(self):
        self.ev = []
        self.act = []
        self.subscribers = {}
        self.data = {}

    def emit(self, event):
        name = event[0]
        reducers = self.subscribers.get(name)
        for r in reducers:
            #TODO: check allowed data for the reducers
            d,a = r(self.data, event)
            self.data.update(d)
            self.dispatch(a)

    def dispatch(self, action):
        self.act.append(action)

    def on(self, name, action):
        self.subs[name] = action


    def get_actions(self):
        return self.act
