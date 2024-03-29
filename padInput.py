
import math
import angleLib
import gamepadLib
import time
import pynput
from os import system
def clearScreen():
    system('cls')

def empty_function(*arg):
    pass

gamepadType = 'xboxOne'

AXIS_HIGH           = 0.70
AXIS_DIFF           = 0.40
TRIGGER_HIGH        = 0.80
PUSH_ANGLE_RANGE    = 15
HOLD_TIME           = 1
RAPID_TIME          = 0.5
MOUSE_SPEED         = 10
MOUSE_SPEED_DASH    = 50
AXIS_ZERO           = 0.2

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
def get_mapping():
    global AXIS_KEY_MAPPING
    return AXIS_KEY_MAPPING

gamepad = {}

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()

def update_gamepad():
    global gamepad
    gamepad = gamepadLib.get_gamepad(gamepadType)

class uiScreen:
    def open_window():
        system('guide.png')
    def close_window():
        # system('guide.png')
        pass

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
        vec = angleLib.coord2vec((gamepad.axis[self.name + 'X'], gamepad.axis[self.name + 'Y']))
        return vec[1]
        
    def get_mag(self):
        global gamepad
        vec = angleLib.coord2vec((gamepad.axis[self.name + 'X'], gamepad.axis[self.name + 'Y']))
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
        sangle = angleLib.get_angle_section(self.started_angle)
        pangle = angleLib.get_angle_section(target_angle)
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

class Trigger:
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
                if gamepad.axis[self.name] > AXIS_HIGH:
                    if time.time() >= self.last_pressed + HOLD_TIME:
                        self.if_hold()
                        self.last_pressed = self.last_pressed + RAPID_TIME - HOLD_TIME
                else:
                    # just released
                    self.is_pressed = False
                    self.if_released()
            else:
                if gamepad.axis[self.name] > AXIS_HIGH:
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
'STA': Button('STA'),
'LT': Trigger('LT'),
'RT': Trigger('RT')
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

def unbind_all_btn(exception=[]):
    for btn in pad_status:
        if (type(pad_status[btn]) == Button or type(pad_status[btn]) == Trigger) and not (btn in exception):
            pad_status[btn].set_clicked_callback(lambda:None)
            pad_status[btn].set_hold_callback(lambda:None)
            pad_status[btn].set_released_callback(lambda:None)

class Input_mode:
    def __init__(self, name='', on=lambda:None, update=lambda:None, type=empty_function):
        self.name = name
        self.on = on
        self.update = update
        self.type = type
        self.sub = None

# type_english(pad_status[side])

def english_update():
    pass
def english_on():
    # if mode is English
    bind_btn_key('S', pynput.keyboard.Key.space)
    bind_btn_key('W', pynput.keyboard.Key.enter)
    bind_btn_key('E', pynput.keyboard.Key.backspace)
    bind_btn_key('N', '.')
    bind_btn_key('LB', pynput.keyboard.Key.shift, False)
    pad_status['LS'].set_clicked_callback(uiScreen.open_window)
def english_type(stick):
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
        key = AXIS_KEY_MAPPING[num][angleLib.section_to_four(angleLib.get_angle_section(stick.started_angle))][stick.spin]
    keyboard.press(key)
    keyboard.release(key)

def mouse_update():
    global mouse
    global gamepad
    
    vec = angleLib.coord2vec((gamepad.axis['LX'], gamepad.axis['LY']))
    if vec[0] > AXIS_ZERO:
        mouse.move(MOUSE_SPEED_DASH*gamepad.axis['LX'], -MOUSE_SPEED_DASH*gamepad.axis['LY'])
    
    vec = angleLib.coord2vec((gamepad.axis['RX'], gamepad.axis['RY']))
    if vec[0] > AXIS_ZERO:
        mouse.move(MOUSE_SPEED*gamepad.axis['RX'], -MOUSE_SPEED*gamepad.axis['RY'])
def mouse_on():
    global mouse
    def left_click():
        mouse.press(pynput.mouse.Button.left)
    def left_release():
        mouse.release(pynput.mouse.Button.left)
    def right_click():
        mouse.press(pynput.mouse.Button.right)
    def right_release():
        mouse.release(pynput.mouse.Button.right)
    pad_status['RB'].set_clicked_callback(left_click)
    pad_status['RB'].set_released_callback(left_release)
    pad_status['RT'].set_clicked_callback(right_click)
    pad_status['RT'].set_released_callback(right_release)
    
    


INPUT_MODE_LIST = {
    'english':  Input_mode('english', english_on, english_update, english_type),
    'mouse':    Input_mode('mouse', mouse_on, mouse_update)
}

INPUT_MODE_ROTATION = [
    INPUT_MODE_LIST['english']
]

INPUT_MODE_LIST['english'].sub = INPUT_MODE_LIST['mouse']

selected_input_mode = INPUT_MODE_ROTATION[0]
current_input_mode = selected_input_mode
current_input_mode.on()

def axis_update():
    global gamepad
    global pad_status
    global AXIS_HIGH
    sides = {'L', 'R'}
    for side in sides:
        coord = (gamepad.axis[side + 'X'], gamepad.axis[side + 'Y'])
        vec = angleLib.coord2vec((gamepad.axis[side + 'X'], gamepad.axis[side + 'Y']))
        mag = vec[0]
        ang = vec[1]
        if not pad_status[side].check_low_to_high():
            if pad_status[side].check_high_to_low():
                global current_input_mode
                current_input_mode.type(pad_status[side])
                pad_status[side].reset()
        
        if pad_status[side].is_high:
            pad_status[side].spin = pad_status[side].check_spin(pad_status[side].get_angle())

def button_update():
    global pad_status
    for btnName in list(pad_status.keys()):
        btn = pad_status[btnName]
        if type(btn) == Button:
            btn.check_pressed()

def trigger_update():
    global pad_status
    for btnName in list(pad_status.keys()):
        btn = pad_status[btnName]
        if type(btn) == Trigger:
            btn.check_pressed()

quitPadInput = False

def toggle_sub_mode():
    global current_input_mode
    global selected_input_mode
    if current_input_mode == selected_input_mode:
        current_input_mode = selected_input_mode.sub
    else:
        current_input_mode = selected_input_mode
    unbind_all_btn(['SEL'])
    current_input_mode.on()
pad_status['SEL'].set_clicked_callback(toggle_sub_mode)

while not quitPadInput:
    update_gamepad()
    axis_update()
    button_update()
    trigger_update()
    # print(time.time())
    # if gamepad['BTN_START'] == 1:
    #     break
    current_input_mode.update()
    time.sleep(0.02)
    






