from itertools import chain

from .BaseModel import BaseModel
class SyncModel(BaseModel):
    """
    This model is the very basic implemetation of ev-reduce api.
    The event generators are merged into a single generator
    and for every event a corresponding reducer is called.

    Everything is going on in a single thread
    """
    def __init__(self):
        super().__init__()

    def start(self):
        """
        Start execution
        """
        gen = chain(*self.sources)
        for ev in gen:
            for act in self._handle_ev(ev):
                self._dispatch(act)

    def _dispatch(self,act):
        self._exec_act(act)
