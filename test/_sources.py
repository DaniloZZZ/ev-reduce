import time

def stdin():
    while True:
        ev = ( 'stdin',
            input('>')
        )
        yield ev

def time():
    while True:
        ev = ( 'time',
	    time.time()
        )
        yield ev
