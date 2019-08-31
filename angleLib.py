
import math


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
    x = m * math.cos(math.radians(a))
    y = m * math.sin(math.radians(a))
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

def section_to_four(section):
    a = ['E', 'N', 'W', 'S']
    return a[section]
def four_to_section(four):
    k = 0
    for i in ['E', 'N', 'W', 'S']:
        if four == i:
            return k
        k = k + 1
    return k
    

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



