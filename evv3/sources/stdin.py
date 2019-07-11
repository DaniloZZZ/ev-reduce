from .. import listAPI
EV_NAME = 'stdin'

if __name__=="__main__":
    api = listAPI()
    while True:
        event = (EV_NAME, input('>'))
        api.emit(event)
