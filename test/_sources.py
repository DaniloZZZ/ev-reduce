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

def time():
    while True:
        ev = ( 'time',
	    time.time()
        )
        yield ev
