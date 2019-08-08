
import xboxOne
import math
from pynput.keyboard import Key, Controller
from os import system
def clearScreen():
    system('cls')


gamepadType = 'xboxOne'

AXIS_HIGH = 70
AXIS_DIFF = 40
TRIGGER_HIGH = 80

AXIS_KEY_MAPPING=[
{
    'east'  : {
        'left'  : 'l',
        'on'    : 'a',
        'right' : 'b',
        'both'  : '.'
    },
    'north' : {
        'left'  : 'w',
        'on'    : 'e',
        'right' : 'h',
        'both'  : '.'
    },
    'west'  : {
        'left'  : 'j',
        'on'    : 'i',
        'right' : 'c',
        'both'  : '.'
    },
    'south' : {
        'left'  : 'f',
        'on'    : 's',
        'right' : 'x',
        'both'  : '.'
    },
},
{
    'east'  : {
        'left'  : 'm',
        'on'    : 'n',
        'right' : 'k',
        'both'  : '.'
    },
    'north' : {
        'left'  : 'g',
        'on'    : 't',
        'right' : 'd',
        'both'  : '.'
    },
    'west'  : {
        'left'  : 'p',
        'on'    : 'o',
        'right' : 'u',
        'both'  : '.'
    },
    'south' : {
        'left'  : 'q',
        'on'    : 'r',
        'right' : 'y',
        'both'  : '.'
    }
}]

getNewEvent = None

if gamepadType == 'xboxOne':
    getNewEvent = xboxOne.getNewEvent
else:
    print('currently, only xboxOne controller is supported')

gamepad = {
'ABS_X': 0,
'ABS_Y': 0,
'ABS_RX': 0,
'ABS_RY': 0,
'BTN_WEST': 0,
'BTN_EAST': 0,
'BTN_SOUTH': 0,
'BTN_NORTH': 0,
'ABS_HAT0Y': 0,
'ABS_HAT0X': 0,
'BTN_TR': 0,
'BTN_TL': 0,
'ABS_RZ': 0,
'ABS_Z': 0,
'BTN_START': 0,
'BTN_SELECT': 0,
'BTN_THUMBR': 0,
'BTN_THUMBL': 0
}


# for keyboard status:
# if axis is zeroed = False
# if axis reach high = angle
# 
# 
# 
# 


padStatus = {
'ABS': False,
'ABS_R': False,
'BTN_WEST': 0,
'BTN_EAST': 0,
'BTN_SOUTH': 0,
'BTN_NORTH': 0,
'ABS_HAT0Y': 0,
'ABS_HAT0X': 0,
'BTN_TR': 0,
'BTN_TL': 0,
'ABS_RZ': 0,
'ABS_Z': 0,
'BTN_START': 0,
'BTN_SELECT': 0,
'BTN_THUMBR': 0,
'BTN_THUMBL': 0
}

keyboard = Controller()



def updateGamepad():
    global gamepad
    events = getNewEvent()
    for a in events:
        gamepad[a[0]]=a[1]
    

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

def bindBtnKey(btn, key):
    if padStatus[btn] == 0 and gamepad[btn] == 1:
        padStatus[btn] = 1
        keyboard.press(key)
    elif padStatus[btn] == 1 and gamepad[btn] == 0:
        padStatus[btn] = 0
        keyboard.release(key)
    
    

def axisType(ang, started, stickID):
    global AXIS_DIFF
    global keyboard
    if ang < 0:
        ang += 360
    if started < 0:
        started += 360
    # debug
    if ang > 360 or started > 360:
        print('EERRROROR')
    
    # section
    sectionID = 'east'
    if started < 45 or started >= 315:
        sectionID = 'east'
    elif started < 135:
        sectionID = 'north'
    elif started < 225:
        sectionID = 'west'
    elif started < 315:
        sectionID = 'south'
    
    # trigger
    triggerID = 'on'
    if gamepad['ABS_Z'] >= TRIGGER_HIGH and gamepad['ABS_RZ'] >= TRIGGER_HIGH:
        triggerID = 'both'
    elif gamepad['ABS_Z'] >= TRIGGER_HIGH:
        triggerID = 'left'
    elif gamepad['ABS_RZ'] >= TRIGGER_HIGH:
        triggerID = 'right'
    else:
        triggerID = 'on'
    
    pressedKey = AXIS_KEY_MAPPING[stickID][sectionID][triggerID]
    keyboard.press(pressedKey)
    keyboard.release(pressedKey)
    

def axisUpdate():
    global gamepad
    global padStatus
    global AXIS_HIGH
    coord = (gamepad['ABS_X'], gamepad['ABS_Y'])
    vec = coord2vec((gamepad['ABS_X'], gamepad['ABS_Y']))
    mag = vec[0]
    ang = vec[1]
    if mag < AXIS_HIGH:
        if padStatus['ABS'] != False:
            axisType(ang, padStatus['ABS'], 0)
            padStatus['ABS'] = False
    else:
        if padStatus['ABS'] == False:
            padStatus['ABS'] = ang
    
    coord = (gamepad['ABS_RX'], gamepad['ABS_RY'])
    vec = coord2vec((gamepad['ABS_RX'], gamepad['ABS_RY']))
    mag = vec[0]
    ang = vec[1]
    if mag < AXIS_HIGH:
        if padStatus['ABS_R'] != False:
            axisType(ang, padStatus['ABS_R'], 1)
            padStatus['ABS_R'] = False
    else:
        if padStatus['ABS_R'] == False:
            padStatus['ABS_R'] = ang
    
    
    
    
    

quitPadInput = False


# maxTest = 0
while not quitPadInput:
    updateGamepad()
    axisUpdate()
    
    
    bindBtnKey('BTN_SOUTH', Key.space)
    bindBtnKey('BTN_WEST', Key.enter)
    bindBtnKey('BTN_EAST', Key.backspace)
    
    
    if gamepad['BTN_TL'] == 1:
        padStatus['BTN_TL'] = 1
        keyboard.press(Key.shift)
    elif padStatus['BTN_TL'] == 1 and gamepad['BTN_TL'] == 0:
        padStatus['BTN_TL'] = 0
        keyboard.release(Key.shift)
    
    if gamepad['BTN_START'] == 1:
        break







