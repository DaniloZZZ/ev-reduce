import evv3 as ev3
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
    _input_mock.sequence([
        'hi','13','213','-214','hd'
    ]*10)
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

