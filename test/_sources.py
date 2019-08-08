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

def time_(delay=0.3, duration=3):
    start = time.time()
    while True:
        now = time.time()
        ev = ( 'time',now-start)
        if now-start > duration: return
        yield ev
        time.sleep(delay)
