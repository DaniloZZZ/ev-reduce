import multiprocessing as mpc
from threading import Thread
from itertools import chain
import time

from  .helpers.logging import log
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

    def _emit(self,ev):
        log.debug(f"Emitting event: {ev}")
        self.to_reducers.send(ev)
    def _dispatch(self,act):
        log.debug(f"Dispatching action: {act}")
        self.to_actions.send(act)

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

        def get_emitter_loop(gen_src):
            def loop():
                for ev in gen_src:
                    print('ev',ev)
                    self._emit(ev)
                    # allow other threads
                    time.sleep(0.)
                print("#Emitter exited. Emitting stop signal")
                self._emit(("_stop",''))
            return loop

        em_threads = []
        for gen in self.sources:
            loop = get_emitter_loop(gen)

            em_thread = Thread(
                target=loop,
                name='Emitter'
            )
            em_thread.start()
            em_threads.append( em_thread )

        while sum([t.is_alive() for t in em_threads]) !=0:
            act = self.from_reducers.recv()
            result = self._exec_act(act)
            time.sleep(0)
            #if result=='_cmd_stop':break
        print("Everything ended")

        p.terminate()
        p.join()
        for thr in em_threads:
            thr.join()
