import evv3 as ev3

def stdin_source():
    while True:
        ev = (
            'stdin',
            input('>')
        )
        yield ev

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

def reducer_overflow(event, data):
    data.setdefault('cumsum',0)
    threshhold = 20
    if data['cumsum'] > threshhold:
        return ("OVERFLOW",""), data

def actor(action):
    act_type = action[0]
    if act_type=='ERROR':
        print("There was an error. Please enter text")

    elif act_type=='SEND':
        print(action[1])
    elif act_type=='OVERFLOW':
        print("Overflow buddy:(")
    else:
        return -1


ev = ev3.SyncModel()
ev.add_source( stdin_source() )
ev.add_actor( actor )

ev.add_reducer( reducer_cumsum , subscribe=['stdin'])
ev.add_reducer( reducer_overflow , subscribe=['stdin'])

ev.start()
