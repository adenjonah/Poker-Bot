from random import choice, randint


def get_response(user_input: str) -> str:
    usermessage = user_input

    if usermessage =='':
        return 'Quiet'
    elif usermessage == 'hello':
        return 'Hey'
    elif usermessage[:7] == 'pb.eval':
        return 'hand evaluation'
    raise NotImplementedError("missing code")