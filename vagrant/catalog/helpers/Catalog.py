import random
import string


def generate_state_token():
    '''
    generate an anti forgery state token
    '''

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    return state
