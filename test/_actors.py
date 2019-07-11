
def printer(action):
    print(action[1])

def printer_bound_to(target):
    def actor(action):
        v = action[1]
        target.append(v)
        print(v)
    return actor
