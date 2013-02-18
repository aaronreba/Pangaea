#!/usr/bin/env python

from math import sqrt
from math import ceil

class CommonException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def screen_coords_from_map(x, y):
    screen_x = x * 45
    screen_y = y * 30
    
    if y & 1 == 1:
        screen_x += 22.5
    
    return (screen_x, screen_y)

def vector_to_pos(current, destination, velocity):
    diffx = destination[0] - current[0]
    diffy = destination[1] - current[1]
    
    diffx2 = diffx * diffx
    diffy2 = diffy * diffy
    
    z2 = (diffx * diffx) + (diffy * diffy)
    z = sqrt(z2)
    
    cosangle
    vx, vy
    
    if z != 0:
        #law of cosines for x velocity
        if diffx != 0:
            cosangle = (diffx2 + z2 - diffy2)
            cosangle = cosangle / (2 * diffx * z)
            vx = cosangle * velocity
        else:
            vx = 0
        
        #law of cosines for y velocity
        if diffy != 0:
            cosangle = (diffy2 + z2 - diffx2)
            cosangle = cosangle / (2 * diffy * z)
            vy = cosangle * velocity
        else:
            vy = 0
        
        return (vx, vy)
    return (0,0)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmm(lcms):
    return reduce(lcm, lcms)

def hex_distance(p0, p1):
    p0_x, p0_y = p0
    p1_x, p1_y = p1
    d_x = abs(p1_x - p0_x)
    d_y = abs(p1_y - p0_y)
    
    if d_y & 1 == 1 and\
            (p0_y & 1 == 1 and p1_x <= p0_x or\
             p0_y & 1 == 0 and p1_x >= p0_x):
        d_x += 1
    
    ceil_d_y = int(ceil(d_y / 2.0))
    
    if d_x <= ceil_d_y:
        return d_y
    else:
        return d_x - ceil_d_y + d_y

def get_adjacent(p):
    adjacent = []
    
    #add left and right sides
    adjacent.append((p[0] - 1, p[1]))
    adjacent.append((p[0] + 1, p[1]))
    
    #2 in front or behind
    adjacent.append((p[0], p[1] - 1))
    adjacent.append((p[0], p[1] + 1))
    
    if p[1] & 1 == 0:
        adjacent.append((p[0] - 1, p[1] - 1))
        adjacent.append((p[0] - 1, p[1] + 1))
    else:
        adjacent.append((p[0] + 1, p[1] - 1))
        adjacent.append((p[0] + 1, p[1] + 1))
    
    return adjacent

def get_direction(p0, p1):
    if hex_distance(p0, p1) != 1:
        raise CommonException('Attempting to get direction when distance is not 1')
    
    p0_x, p0_y = p0
    p1_x, p1_y = p1
    
    dx = p0_x - p1_x
    dy = p0_y - p1_y
    
    if p0_y & 1 == 0:
        #is even
        if dx == 0 and dy == 1:
            return 1
        elif dx == -1 and dy == 0:
            return 3
        elif dx == 0 and dy == -1:
            return 5
        elif dx == 1 and dy == -1:
            return 7
        elif dx == 1 and dy == 0:
            return 9
        else:
            return 11
    else:
        #odd
        if dx == -1 and dy == 1:
            return 1
        elif dx == -1 and dy == 0:
            return 3
        elif dx == -1 and dy == -1:
            return 5
        elif dx == 0 and dy == -1:
            return 7
        elif dx == 1 and dy == 0:
            return 9
        else:
            return 11

def invert_oclock(invert_me):
    if invert_me < 6:
        return invert_me + 6
    else:
        return invert_me - 6
