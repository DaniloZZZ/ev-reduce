import time
import ev_reduce as ev3
import _sources as _src
import _actors as _act
import _input_mock

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

def test_counter():
    return
    _input_mock.sequence([
        'hi','13','213','-214','hd'
    ]*1)
    ev = ev3.MprocModel()

    @ev.reducer( subscribe=['stdin'] )
    def reducer_overflow(event, data):
        data.setdefault('cumsum',0)
        threshhold = 20
        if data['cumsum'] > threshhold:
            return ("OVERFLOW",""), data

    @ev.actor('ERROR')
    def err(act):
        print("There was an error. Please enter text")

    @ev.actor('OVERFLOW')
    def overf(act):
        print("Overflow buddy:(")

    outputs=[]
    ev.actor('SEND')( _act.printer_bound_to(outputs) )

    ev.source( _src.stdin )()

    # could use decorator too
    ev.add_reducer( reducer_cumsum , subscribe=['stdin'])

    ev.start()
    print("<",outputs)
    assert outputs == [
        'Sum is 13',
        'Sum is 226',
        'Sum is 12',
    ]

    _input_mock.restore()

def test_async():
    #return
    _input_mock.sequence([
        'hi','13','213','-214','hd'
    ]*1)
    # try to change this to Sync model
    #ev = ev3.SyncModel()
    ev = ev3.MprocModel()

    @ev.reducer( subscribe=['stdin'] )
    def reducer_overflow(event, data):
        data.setdefault('cumsum',0)
        threshhold = 20
        if data['cumsum'] > threshhold:
            return ("OVERFLOW",""), data

    @ev.actor('ERROR')
    def err(act):
        print("There was an error. Please enter text")
        print('_waiting...')
        time.sleep(0.7)

    @ev.actor('OVERFLOW')
    def overf(act):
        print("Overflow buddy:(")

    outputs=[]
    ev.actor('SEND')( _act.printer_bound_to(outputs) )

    ev.source( _src.stdin )()
    ev.source( _src.time_ )()
    ev.source( _src.time_ )(delay=1)
    print(0, ev.sources)

    @ev.reducer(subscribe=['time'])
    def reducer_time(ev,d):
        return ("SEND",'time is:'+str(ev[1])), {'time':ev[1]}

    # could use decorator too
    ev.add_reducer( reducer_cumsum , subscribe=['stdin'])

    ev.start()
    #print("<",outputs)

    _input_mock.restore()
