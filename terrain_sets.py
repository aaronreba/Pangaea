#!/usr/bin/env python

#map values:
#(('type', temp, precip, ??), [walkable, empty, see-through], [items])

#mask values:
#(temp, precip, ??)

def make_terrain_test(scheme):
    #10x15 map
    if scheme == 'basic_grass':
        game_map = {}
        game_map_chunk_mask = {}
        for x in xrange(10):
            for y in xrange(15):
                game_map[x, y] = (('grass', 0, 0, 0), [True, True, True], [])
        for x in xrange(2):
            for y in xrange(3):
                game_map_chunk_mask[x, y] = (0, 0, 0)
        return (game_map, game_map_chunk_mask, ((0, 10), (0, 15)))