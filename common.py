#!/usr/bin/env python

from math import sqrt

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
    