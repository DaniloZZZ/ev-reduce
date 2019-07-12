import time

def stdin():
    while True:
        try:
            ev = ( 'stdin',
                input('>')
            )
        except KeyboardInterrupt:
            return
        yield ev

def time_():
    start = time.time()
    while True:
        now = time.time()
        ev = ( 'time',now-start)
        if now-start >2: return
        yield ev
        time.sleep(0.3)
