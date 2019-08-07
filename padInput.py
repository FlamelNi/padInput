
import xboxOne
import math
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
        'right' : 'b'
    },
    'north' : {
        'left'  : 'w',
        'on'    : 'e',
        'right' : 'h'
    },
    'west'  : {
        'left'  : 'j',
        'on'    : 'i',
        'right' : 'c'
    },
    'south' : {
        'left'  : 'f',
        'on'    : 's',
        'right' : 'x'
    },
},
{
    'east'  : {
        'left'  : 'm',
        'on'    : 'n',
        'right' : 'k'
    },
    'north' : {
        'left'  : 'g',
        'on'    : 't',
        'right' : 'd'
    },
    'west'  : {
        'left'  : 'p',
        'on'    : 'o',
        'right' : 'u'
    },
    'south' : {
        'left'  : 'q',
        'on'    : 'r',
        'right' : 'y'
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


axisStatus = {
'ABS': False,
'ABS_R': False#,
# 'BTN_WEST': 0,
# 'BTN_EAST': 0,
# 'BTN_SOUTH': 0,
# 'BTN_NORTH': 0,
# 'ABS_HAT0Y': 0,
# 'ABS_HAT0X': 0,
# 'BTN_TR': 0,
# 'BTN_TL': 0,
# 'ABS_RZ': 0,
# 'ABS_Z': 0,
# 'BTN_START': 0,
# 'BTN_SELECT': 0,
# 'BTN_THUMBR': 0,
# 'BTN_THUMBL': 0
}

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


def axisType(ang, started, stickID):
    global AXIS_DIFF
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
    
    # spin
    spinID = 'on'
    diff = started - ang
    if diff > 180:
        diff = -360 - diff
    elif diff < -180:
        diff = 360 - diff
    if abs(diff) < AXIS_DIFF:
        spinID = 'on'
    elif diff > AXIS_DIFF:
        spinID = 'right'
    elif diff < AXIS_DIFF:
        spinID = 'left'
    else:
         print('error')
    
    print(AXIS_KEY_MAPPING[stickID][sectionID][spinID])
    

def axisUpdate():
    global gamepad
    global axisStatus
    global AXIS_HIGH
    coord = (gamepad['ABS_X'], gamepad['ABS_Y'])
    vec = coord2vec((gamepad['ABS_X'], gamepad['ABS_Y']))
    mag = vec[0]
    ang = vec[1]
    if mag < AXIS_HIGH:
        if axisStatus['ABS'] != False:
            axisType(ang, axisStatus['ABS'], 0)
            axisStatus['ABS'] = False
    else:
        if axisStatus['ABS'] == False:
            axisStatus['ABS'] = ang
    
    coord = (gamepad['ABS_RX'], gamepad['ABS_RY'])
    vec = coord2vec((gamepad['ABS_RX'], gamepad['ABS_RY']))
    mag = vec[0]
    ang = vec[1]
    if mag < AXIS_HIGH:
        if axisStatus['ABS_R'] != False:
            axisType(ang, axisStatus['ABS_R'], 1)
            axisStatus['ABS_R'] = False
    else:
        if axisStatus['ABS_R'] == False:
            axisStatus['ABS_R'] = ang
    
    
    
    
    

quitPadInput = False


# maxTest = 0
while not quitPadInput:
    updateGamepad()
    axisUpdate()
    # print(gamepad['BTN_SOUTH'])
    # if maxTest < math.sqrt(gamepad['ABS_X']**2 + gamepad['ABS_Y']**2):
    #     maxTest = math.sqrt(gamepad['ABS_X']**2 + gamepad['ABS_Y']**2)
    if gamepad['BTN_SOUTH'] == 1:
        clearScreen()
    #     print(maxTest)
    #     maxTest = 0
    
    if gamepad['BTN_START'] == 1:
        break







