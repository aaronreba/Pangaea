#!/usr/bin/env python

from math import sqrt
from math import ceil

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
    p0x, p0y = p0
    p1x, p1y = p1
    dx = abs(p1x - p0x)
    dy = abs(p1y - p0y)
    
    if dy & 1 == 1 and\
            (p0y & 1 == 1 and p1x <= p0x or\
             p0y & 1 == 0 and p1x >= p0x):
        dx += 1
    
    if dx <= ceil(dy / 2.0):
        return dy
    else:
        return int(dx - ceil(dy / 2.0) + dy)

