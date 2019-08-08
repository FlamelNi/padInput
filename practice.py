
from pynput import keyboard
import random
from os import system
def clearScreen():
    system('cls')

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

EASY_LIST=[
'arisen',
'insert',
'nitro',
'orient',
'reason',
'stone',
'train',
'near',
'noise',
'saint',
'stain',
'sonar',
'anti',
'earn',
'iron',
'ion',
'neat',
'nest',
'test',
'rain',
'rant',
'rent',
'tent',
'torn',
'art',
'ear',
'rise',
'star',
'tear'
]

DIFFICULTY = 1
casual = True

keyList = []
buttonList = ['east','west','north','south']
if DIFFICULTY >= 0:
    for a in range(0,2):
        for btn in buttonList:
            keyList.append(AXIS_KEY_MAPPING[a][btn]['on'])
if DIFFICULTY >= 1:
    for a in range(0,2):
        for btn in buttonList:
            keyList.append(AXIS_KEY_MAPPING[a][btn]['left'])
if DIFFICULTY >= 2:
    for a in range(0,2):
        for btn in buttonList:
            keyList.append(AXIS_KEY_MAPPING[a][btn]['right'])

print(keyList)


def flush():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    

# Collect events until released
quitLoop = False
target = 0
if casual:
    target = keyList[random.randint(0, len(keyList)-1)]
def on_press(key):
    global target
    if key == keyboard.Key.esc:
        global quitLoop
        quitLoop = True
        return False
    if str(key.char) == str(target):
        clearScreen()
        target = keyList[random.randint(0, len(keyList)-1)]
        print(target)
    else:
        print('!')
    
    
    return False
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

print(target)
while not quitLoop:
    if casual:
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
        
        flush()
    else:
        if target == 0:
            target = EASY_LIST[random.randint(0, len(EASY_LIST)-1)]
        print(target)
        b = input()
        if target == b:
            target = 0
        clearScreen()
        
    




