#!/usr/bin/env python

#map values:
#(('type', temp, precip, ??), [walkable, empty, see-through], [items])

#mask values:
#(temp, precip, ??)

import terraform

def make_terrain_test(scheme):
    #10x15 map
    if scheme == 'basic_grass':
        landscape = terraform.landscape()
        for x in xrange(10):
            for y in xrange(15):
                landscape.landscape[x, y] = (('grass', 0, 0, 0), [True, True, True], [])
        for x in xrange(2):
            for y in xrange(3):
                landscape.landscape_chunk_mask[x, y] = (0, 0, 0)
        landscape.landscape_size = ((0, 10), (0, 15))
        return landscape
