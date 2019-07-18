import multiprocessing as mpc
from threading import Thread
from itertools import chain
import time

from .BaseModel import BaseModel

def _pipe_reader(pipe_end):
    while True:
        yield pipe_end.recv()

class MprocModel(BaseModel):
    """
    Sources and actions go in main process, but in different threads.

    Reducers go in other process.

    Communication is performed with two pipes: source-reducer and reducer-sourcce
    """
    def __init__(self):
        super().__init__()
        self.to_reducers, self.from_source = mpc.Pipe()
        self.from_reducers, self.to_actions = mpc.Pipe()

    def start(self):
        """
        Start execution
        """
        def reducers_loop():
            gen = _pipe_reader(self.from_source)
            for ev in gen:
                for act in self._handle_ev(ev):
                    self._dispatch(act)
        p = mpc.Process(
            target=reducers_loop,
            args=(),
            name='Reducer'
        )
        p.start()

        gen_src = chain(*self.sources)
        def emitter_loop():
            for ev in gen_src:
                self._emit(ev)
                # allow other threads
                time.sleep(0.)
            print("#Emitter exited. Emitting stop signal")
            self._emit(("_stop",''))

        emitter = Thread( 
            target=emitter_loop,
            name='Emitter'
        )
        emitter.start()

        while True:
            act = self.from_reducers.recv()
            result = self._exec_act(act)
            time.sleep(0)
            if result=='_cmd_stop':break

        p.terminate()
        p.join()
        emitter.join()
