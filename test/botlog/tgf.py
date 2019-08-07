import json, time
from loguru import logger as log
from pprint import pprint

folder = './test/botlog/'

"""
    Load the files
"""

trigs = [
    {'predicates': ['comparer.regexp'],
     'attributes': {'text': '1'},
     'block': {'id': 0}},
    {'predicates': ['state.source'],
     'attributes': {'source': 0},
     'block': {'id': 1}},
    {'predicates': ['comparer.equals'],
     'attributes': {'text': '/start'},
     'block': {'id': 2}}
]

blocks = [
    {'id': 0,
     'actions': ['message.send'],
     'attributes': {'pagename': '', 'extra': '', 'text': 'You pressed 1'}},
    {'id': 1,
     'actions': ['message.send'],
     'attributes': {'pagename': '', 'extra': '', 'text': 'Welcome'}},
    {'id': 2,
     'actions': ['message.send'],
     'attributes': {'pagename': '', 'extra': '', 'text': 'you started'}}
]

try:
    trigs = json.load(open(folder+'index-triggers.json'))
    blocks = json.load(open(folder+'index-blocks.json'))
except FileNotFoundError as e:
    log.error(f"Failed to open some files: {str(e)}, using default")


"""
params:
    event, data, attributes
"""
PREDICATES={
    'state.source':lambda *x: x[1]['state']==x[2]['source'], #match state
    'comparer.equals':lambda *x: x[0][1]==x[2]['text'], #match text from input
    'comparer.regexp':lambda *x: x[0][1]==x[2]['text'], #match text from input
    'any':lambda *x: True,
}
"""
params:
    data
return:
    dict: state update
"""
ACTORS ={
    'print':        lambda x: print(x['text']),
    'message.send': lambda x: print('>>>',x['text']),
    'analytics':lambda x: print('analytics',x['page']),
    'state.set':lambda x: {'state':x['state']}
}

b_dict ={}
for b in blocks:
    b_dict[b['id']]=b
blocks = b_dict

class Tgfv2:
    def __init__(self, triggers, actions):
        pprint('triggers:')
        pprint(triggers)
        pprint('blocks:')
        pprint(actions)

        self.trigs = triggers
        self.actions = actions
        self.data = {
            'state':None
        }

    def _get_next_block(self, event, data):
        block_id = None
        for t in self.trigs:
            cum = 0
            bools =  [
                PREDICATES.get(pred_name, lambda *x:False)
                (event, self.data, t['attributes'])
                for pred_name in t['predicates']
            ]
            if sum(bools)==len(bools):
                block_id = t.get('block', {}).get('id')
        block = self.actions.get(block_id)
        return block

    def __call__(self, event, data):
        block = self._get_next_block(event, data)
        if block:
            log.debug('triggered trns to', block['id'])
            self.data['state'] = block['id']
            for ac_name in block['actions']:
                actor =  ACTORS.get(ac_name)
                upd_dict = actor( block['attributes'] )
                # TODO: store data in data from ev
                if upd_dict:
                    self.data.update(upd_dict)
                return ('tgf','new_state'), {}
        return ("tgf", 'noaction'), {}

import time
import ev_reduce as ev3
from _sources import stdin

def test_tgf():
    tgf=Tgfv2(trigs, blocks)
    ev = ev3.MprocModel()
    ev.add_source(stdin())
    def new_state():
        state = None
        while True:
            state = yield 'new_state', state
            print("sent ns for ", state)
    # Create and start gen
    new_state_gen = new_state()
    next(new_state_gen)
    ev.add_source(new_state_gen)
    ev.add_reducer( tgf, subscribe=['stdin', 'new_state'])


    @ev.actor('tgf')
    def status_logger(event):
        print("tgf ev:",event[1])
        if event[1]=='new_state':
            new_state_gen.send(event[1])

    ev.start()

