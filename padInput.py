
import xboxOne
import math
import gamepadLib
import time
from pynput.keyboard import Key, Controller
from os import system
def clearScreen():
    system('cls')

gamepadType = 'xboxOne'

AXIS_HIGH           = 0.70
AXIS_DIFF           = 0.40
TRIGGER_HIGH        = 0.80
PUSH_ANGLE_RANGE    = 15
HOLD_TIME           = 1
RAPID_TIME          = 0.5

AXIS_KEY_MAPPING=[
{
    'E'  : {
        'L'  : 'l',
        ''    : 'a',
        'R' : 'b'
    },
    'N' : {
        'L'  : 'w',
        ''    : 'e',
        'R' : 'h'
    },
    'W'  : {
        'L'  : 'j',
        ''    : 'i',
        'R' : 'c'
    },
    'S' : {
        'L'  : 'f',
        ''    : 's',
        'R' : 'x'
    },
},
{
    'E'  : {
        'L'  : 'm',
        ''    : 'n',
        'R' : 'k'
    },
    'N' : {
        'L'  : 'g',
        ''    : 't',
        'R' : 'd'
    },
    'W'  : {
        'L'  : 'p',
        ''    : 'o',
        'R' : 'u'
    },
    'S' : {
        'L'  : 'q',
        ''    : 'r',
        'R' : 'y'
    }
}]

gamepad = {}

keyboard = Controller()

def update_gamepad():
    global gamepad
    gamepad = gamepadLib.get_gamepad(gamepadType)


def coord2vec(coord):
    x = coord[0]
    y = coord[1]
    m = math.sqrt(x**2 + y**2)
    a = 0
    if m < 0.01:
        a = False
    else:
        a = math.degrees(math.acos(x/m))
    if y < 0:
        a = 360 - a
    return (m,a)

def vec2coord(vec):
    m = vec[0]
    a = vec[1]
    x = m * math.cos(radians(a))
    y = m * math.sin(radians(a))
    return (x,y)


def angle_overflow(angle):
    # in degrees
    if angle < 0:
        angle += 360
    if angle >= 360:
        angle -= 360
    return angle

'''
    1
2       0
    3
'''

def section_to_4(section):
    a = ['E', 'N', 'W', 'S']
    return a[section]

def get_angle_section(angle):
    # in degrees
    section = -1
    if angle < 45 or angle >= 315:
        section = 0
    elif angle >= 45 and angle < 135:
        section = 1
    elif angle >= 135 and angle < 225:
        section = 2
    elif angle >= 225 and angle < 315:
        section = 3
    else:
        print('ERROR')
    return section

def type_english(stick):
    global keyboard
    key = ''
    if stick.spin == 'B':
        if stick.name == 'L':
            key = 'v'
        elif stick.name == 'R':
            key = 'z'
    else:
        num = -1
        if stick.name == 'L':
            num = 0
        elif stick.name == 'R':
            num = 1
        key = AXIS_KEY_MAPPING[num][section_to_4(get_angle_section(stick.started_angle))][stick.spin]
    keyboard.press(key)
    keyboard.release(key)
    
class Stick:
    def __init__(self, name=''):
        self.name           = name
        self.is_high        = False
        self.started_angle  = False
        self.pushing_angle  = False
        self.spin           = ''
        self.status         = 0
    
    def get_angle(self):
        global gamepad
        vec = coord2vec((gamepad.axis[self.name + 'X'], gamepad.axis[self.name + 'Y']))
        return vec[1]
        
    def get_mag(self):
        global gamepad
        vec = coord2vec((gamepad.axis[self.name + 'X'], gamepad.axis[self.name + 'Y']))
        return vec[0]
        
    def check_low_to_high(self):
        global AXIS_HIGH
        if not self.is_high and self.get_mag() >= AXIS_HIGH:
            self.started_angle = self.get_angle()
            self.is_high = True
            self.spin = ''
            self.status = 1
            return True
        return False
    def check_high_to_low(self):
        global AXIS_HIGH
        if self.is_high and self.get_mag() < AXIS_HIGH:
            self.is_high = False
            return True
        return False
    def reset(self):
        self.status = 0
        self.spin = ''
    def check_spin(self,target_angle):
        sangle = get_angle_section(self.started_angle)
        pangle = get_angle_section(target_angle)
        if pangle - sangle == 1 or pangle - sangle == -3:
            return 'L'
        elif pangle - sangle == -1 or pangle - sangle == 3:
            return 'R'
        elif pangle - sangle == -2 or pangle - sangle == 2:
            return 'B'
        else:
            return ''

class Button:
    def __init__(self, name=''):
        self.name           = name
        self.is_pressed     = False
        self.last_pressed   = 0
        self.status         = 0
        self.if_clicked     = lambda: None
        self.if_released    = lambda: None
        self.if_hold        = lambda: None
    def set_clicked_callback(self, funct):
        self.if_clicked = funct
    def set_released_callback(self, funct):
        self.if_released = funct
    def set_hold_callback(self, funct):
        self.if_hold = funct
    def callback_reset(self):
        self.if_clicked     = lambda: None
        self.if_released    = lambda: None
        self.if_hold        = lambda: None
    def check_pressed(self):
        if self.is_pressed:
            if gamepad.btn[self.name]:
                if time.time() >= self.last_pressed + HOLD_TIME:
                    self.if_hold()
                    self.last_pressed = self.last_pressed + RAPID_TIME - HOLD_TIME
            else:
                # just released
                self.is_pressed = False
                self.if_released()
        else:
            if gamepad.btn[self.name]:
                self.last_pressed = time.time()
                self.is_pressed = True
                self.if_clicked()

pad_status = {
'L': Stick('L'),
'R': Stick('R'),
'N': Button('N'),
'S': Button('S'),
'W': Button('W'),
'E': Button('E'),
'LB': Button('LB'),
'RB': Button('RB'),
'LS': Button('LS'),
'RS': Button('RS'),
'SEL': Button('SEL'),
'STA': Button('STA')
}

def bind_btn_key(btn, key, rapid_hold=True):
    
    if rapid_hold:
        def clicked():
            keyboard.press(key)
            keyboard.release(key)
        pad_status[btn].set_clicked_callback(clicked)
        
        pad_status[btn].set_hold_callback(clicked)
    else:
        def clicked():
            keyboard.press(key)
        def released():
            keyboard.release(key)
        pad_status[btn].set_clicked_callback(clicked)
        pad_status[btn].set_released_callback(released)
        
    
    return False

# if mode is English
bind_btn_key('S', Key.space)
bind_btn_key('W', Key.enter)
bind_btn_key('E', Key.backspace)
bind_btn_key('LB', Key.shift, False)

def axis_update():
    global gamepad
    global pad_status
    global AXIS_HIGH
    sides = {'L', 'R'}
    for side in sides:
        coord = (gamepad.axis[side + 'X'], gamepad.axis[side + 'Y'])
        vec = coord2vec((gamepad.axis[side + 'X'], gamepad.axis[side + 'Y']))
        mag = vec[0]
        ang = vec[1]
        if not pad_status[side].check_low_to_high():
            if pad_status[side].check_high_to_low():
                # if mode is English:
                type_english(pad_status[side])
                pad_status[side].reset()
        
        if pad_status[side].is_high:
            pad_status[side].spin = pad_status[side].check_spin(pad_status[side].get_angle())

def button_update():
    for btnName in list(pad_status.keys()):
        btn = pad_status[btnName]
        if type(btn) == Button:
            btn.check_pressed()
    


quitPadInput = False


# maxTest = 0
while not quitPadInput:
    update_gamepad()
    axis_update()
    button_update()
    
    # if gamepad['BTN_START'] == 1:
    #     break
    
    time.sleep(0.02)
    







