__input = None

def sequence(seq):
    global __input
    __input = __builtins__['input']

    gen = (inp for inp in seq)
    def fake_input(x):
        try:
            v = next(gen)
        except StopIteration:
            raise KeyboardInterrupt
        print("$>",v)
        return v
    __builtins__['input']=fake_input

def restore():
    if __input is not None:
        __builtins__['input']=__input
