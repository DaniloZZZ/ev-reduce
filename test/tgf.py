import time
import evv3 as ev3


PREDS = {
    'state.equals':
}

class Tgfv2:
    def __init__(self, ui):
        self.UI = ui
        self.triggers = []

    def add_trigger(self, trg):
        self.triggers.append( trg )

    def __call__(self, event, data):
        state = data['state']
        for t in self.triggers:
            pred = PREDS[t]


def test_tgf():
    pass

