
from inputs import get_gamepad

def init():
    
    inputContainer = {}

    # class gamepadAttribute:
    #     ev_type = ''
    #     code = ''
    #     state = ''
    #     def __init__(self, event = None):
    #         if event is not None:
    #             # self.ev_type = event.ev_type
    #             self.code    = event.code
    #             self.state   = event.state


    while 1:
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Key' or event.ev_type == 'Absolute':
                inputContainer[event.code] = event.state
                print('\n\n\n\n\n')
                i = 0
                for a in list(inputContainer.keys()):
                    print(str(a) + ': ' + str(inputContainer[a]) )



            # print('evType:'+str(event.ev_type))
            # print('code:'  +str(event.code))
            # print('state:' +str(event.state))
            # print('\n')

'''
ABS_Y: -158
ABS_RY: -3261
ABS_RX: -157
ABS_X: 706
BTN_THUMBR: 0
BTN_THUMBL: 0
ABS_HAT0Y: 0
ABS_HAT0X: 0
BTN_START: 0
BTN_SELECT: 0
BTN_SOUTH: 0
BTN_EAST: 0
BTN_NORTH: 0
BTN_WEST: 0
BTN_TR: 0
ABS_RZ: 0
BTN_TL: 0
ABS_Z: 0
'''


