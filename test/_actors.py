
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

