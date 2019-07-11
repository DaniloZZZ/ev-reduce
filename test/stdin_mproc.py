import evv3 as ev3
import _sources as _src
import _actors as _act

ev = ev3.MprocModel()


def reducer_cumsum(event, data):
    """ Parse int from the input then add to 'cumsum data' """
    text = event[1]
    val = 0
    try:
        val=int(text)
    except Exception as e:
        action =('ERROR', 'not an int')
        return action, {}

    data.setdefault('cumsum',0)
    data['cumsum'] += val

    return ("SEND",f"Sum is {data['cumsum']}"), data

@ev.reducer( subscribe=['stdin'] )
def reducer_overflow(event, data):
    data.setdefault('cumsum',0)
    threshhold = 20
    if data['cumsum'] > threshhold:
        return ("OVERFLOW",""), data

ev.actor( _act.actor )

ev.source( _src.stdin )()


# could use decorator too
ev.add_reducer( reducer_cumsum , subscribe=['stdin'])

ev.start()
