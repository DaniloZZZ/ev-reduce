import time

trigs = {
    1:{
        'predicates':['any'],
        'params':{ },
        'action':2
    } ,
    2:{
        'predicates':['state.equals', 'text.equals'],
        'params':{ 'state':'bar','text':'exit' },
        'action':1,
    },
    3:{
        'predicates':['state.equals'],
        'params':{'state':0 },
        'action':'set_state_bar'
    } }

actions = {
    1:{
        'action':"print",
        'params':{ 'text':'Why yo try to exit?' }
    },
    'set_state_bar':{
        'action':'state.set',
        'params':{'state':'bar'}
    },
    2:{
        'action':"analytics",
        'params':{ 'page':'anypage' }
    } }


"""
 params:
    event, data, params
"""
PREDICATES={
    'state.equals':lambda *x: x[1]['state']==x[2]['state'], #match state
    'text.equals':lambda *x: x[0][1]==x[2]['text'], #match text from input
    'any':lambda *x: True,
}
ACTORS ={
    'print':lambda x: print(x['text']),
    'analytics':lambda x: print('analytics',x['page']),
    'state.set':lambda x: {'state':x['state']}
}

class Tgfv2:
    def __init__(self, triggers, actions):
        self.trigs = triggers
        self.actions = actions
        self.data = {
            'state':0
        }

    def __call__(self, event, data):
        action_name = None
        for t in self.trigs.values():
            print("tf", t)
            cum = 0
            for pred_name in t['predicates']:
                pred = PREDICATES.get(pred_name)
                if not pred: continue
                #print("d",self.data, t['params'])
                label = pred(event, self.data, t['params'])
                print('l', label)
                print('l', cum)
                cum += 1-int(label)
            if cum==0:
                action_name = t['action']
        #print('a', action_name)
        action = self.actions.get(action_name)
        if action:
            actor =  ACTORS.get(action['action'])
            if actor:
                upd_dict = actor( action['params'] )
                # TODO: store data in data from ev
                if upd_dict:
                    self.data.update(upd_dict)
                return ('tgf',0), {}
        return ("tgf",-1), {}

import time
import ev_reduce as ev3
from _sources import stdin

def test_tgf():
    tgf=Tgfv2(trigs, actions)
    ev = ev3.MprocModel()
    ev.add_reducer( tgf, subscribe=['stdin'])
    ev.add_source(stdin())
    @ev.actor('tgf')
    def status_logger(event):
        print("tgf status:",event[1])
    ev.start()

