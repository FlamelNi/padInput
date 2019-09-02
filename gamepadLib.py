import pygame

class Gamepad:
    class Device_map:
        def __init__(self):
            self.axis = {
            'LX': 0,
            'LY': 0,
            'RX': 0,
            'RY': 0,
            'LT': 0,
            'RT': 0
            }
            self.hat = {
            'num': 0,
            'X': 0,
            'Y': 0
            }
            self.btn = {
            'N': 0,
            'S': 0,
            'W': 0,
            'E': 0,
            'LB': 0,
            'RB': 0,
            'LS': 0,
            'RS': 0,
            'SEL': 0,
            'STA': 0
            }
            self.extraTranslate = False#extra function if needed
            self.scale = False
    axis = {}
    hat = {}
    btn = {}
    status = {}
    
    xboxOne_map = Device_map()
    xboxOne_map.axis = {
    'LX': 0,
    'LY': 1,
    'RX': 3,
    'RY': 4,
    'LT': 2,
    'RT': 5
    }
    xboxOne_map.hat = {
    'num': 0,
    'X': 0,
    'Y': 1
    }
    xboxOne_map.btn = {
    'N': 3,
    'S': 0,
    'W': 2,
    'E': 1,
    'LB': 4,
    'RB': 5,
    'LS': 8,
    'RS': 9,
    'SEL': 6,
    'STA': 7
    }
    def xboxOne_map_scale():
        Gamepad.axis['LY'] *= -1
        Gamepad.axis['RY'] *= -1
        Gamepad.axis['LT'] = Gamepad.axis['LT'] / 2 + 0.5
        Gamepad.axis['RT'] = Gamepad.axis['RT'] / 2 + 0.5
    xboxOne_map.scale = xboxOne_map_scale
    
    def get_new_event(dmap=Device_map()):
        j = pygame.joystick.Joystick(0)
        j.init()
        newEvents = pygame.event.get()
        
        # axis
        for i in dmap.axis.keys():
            Gamepad.axis[i] = j.get_axis(dmap.axis[i])
        # btn
        for i in dmap.btn.keys():
            Gamepad.btn[i] = j.get_button(dmap.btn[i])
        # hat
        for i in dmap.hat.keys():
            if i == 'num':
                continue
            Gamepad.hat[i] = j.get_hat(dmap.hat['num'])[dmap.hat[i]]
        if dmap.extraTranslate is not False:
            dmap.extraTranslate()
        if dmap.scale is not False:
            dmap.scale()
        # j.quit()
    

pygame.init()
pygame.joystick.init()
j = False

def quit():
    global j
    if j is not False:
        j.quit()
        j = False
    pygame.joystick.quit()
    pygame.quit()

# 
def get_gamepad(padtype):
    if padtype == 'xboxOne':
        Gamepad.get_new_event(Gamepad.xboxOne_map)
    else:
        print('Error: invalid padtype')
        return False
    return Gamepad



