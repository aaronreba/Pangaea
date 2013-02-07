import random

##########
# to do: #
##########

#integrate random gened items
#add random structures (towns, shrines, fountains, temples, etc)
#take track of when human goes out of range, delete old terrain

#########

#all chunks within this many distance units from the human must be
#generated whenever a generation is requested
#testing: 30 chunks
do_chunk_generate_distance = 2

#a generation is requested when the human is within this many
#chunks from the edge of the world.
#when the human reaches the boundary of this region,
#another check for land is made. if that request can be carried out,
#it will.
#testing: 12 chunks
check_chunk_generate_distance = 2

chunk_size = 5

biome_graph = {}
biome_graph[(-4, -2), (-4, -1)] = 'tundra'
biome_graph[(-4, -2), (0, 4)]   = 'forest'

biome_graph[(-1, 1),  (-4, -3)] = 'desert'
biome_graph[(-1, 1),  (-2, -1)] = 'plains'
biome_graph[(-1, 1),  (0, 2)]   = 'grass'
biome_graph[(-1, 1),  (3, 4)]   = 'heavy_grass'

biome_graph[(2, 4),   (-4, -1)] = 'desert'
biome_graph[(2, 4),   (0, 2)]   = 'grass'
biome_graph[(2, 4),   (3, 4)]   = 'jungle'


#get ungenerated in given distance
def find_immediate_ungenerated(
    game_map,
    game_map_chunk_mask,
    center_position,
    given_distance):
    
    #if surrounding check_distance chunks in each direction are not generated,
    #generate them.
    center_chunk_position = (
        center_position[0] / chunk_size,
        center_position[1] / chunk_size)
    
    neg_x = center_chunk_position[0] - given_distance
    neg_y = center_chunk_position[1] - given_distance
    pos_x = center_chunk_position[0] + given_distance
    pos_y = center_chunk_position[1] + given_distance
    
    #determine generated
    generated_chunks = set(game_map_chunk_mask.keys())
    
    all_check_chunks = set()
    for x in xrange(neg_x, pos_x + 1):
        for y in xrange(neg_y, pos_y + 1):
            all_check_chunks.add((x, y))
    
    #and ungenerated
    ungenerated_chunks = all_check_chunks - generated_chunks
    
    return ungenerated_chunks

#ignorant of checking, assumes that terrain must be generated.
#assumes ungenerated_chunks are all the ungenerated_chunks to be generated
def extend_map_using_ungenerated(
    game_map,
    game_map_chunk_mask,
    ungenerated_chunks):
    
    ##################################
    # determine shape of ungenerated #
    ##################################
    #if it touches an ungenerated edge, generate from generated part
    #cases:
    #1. if 3 sides are ungenerated and one is,
    #generate from what is generated
    #2. if all 4 sides are generated and middle is ungenerated,
    #generate from random piece of generated territory.
    
    #if a chunk touches this many chunks or more (less than or equal
    #to 0 chunks), generate that chunk first
    generate_for_touch = 4
    
    while len(ungenerated_chunks) > 0:
        touching_threshold = []
        for ungenerated_chunk in ungenerated_chunks:
            border_chunk_positions = set([(ungenerated_chunk[0], ungenerated_chunk[1] - 1),
                                          (ungenerated_chunk[0], ungenerated_chunk[1] + 1),
                                          (ungenerated_chunk[0] - 1, ungenerated_chunk[1]),
                                          (ungenerated_chunk[0] + 1, ungenerated_chunk[1])])
            bordering = 0
            for border_chunk in border_chunk_positions:
                if border_chunk in game_map_chunk_mask:
                    bordering += 1
            if 4 >= bordering >= generate_for_touch:
                touching_threshold.append(ungenerated_chunk)
        
        for ungenerated_chunk in touching_threshold:
            generate_chunk(
                game_map,
                game_map_chunk_mask,
                ungenerated_chunk)
            ungenerated_chunks.remove(ungenerated_chunk)
        
        if len(touching_threshold) == 0:
            generate_for_touch -= 1
        else:
            generate_for_touch = 4
    
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    
    for position in game_map.keys():
        if min_x == None:
            min_x = position[0]
        elif min_x > position[0]:
            min_x = position[0]
        
        if max_x == None:
            max_x = position[0]
        elif max_x < position[0]:
            max_x = position[0]
        
        if min_y == None:
            min_y = position[1]
        elif min_y > position[1]:
            min_y = position[1]
        
        if max_y == None:
            max_y = position[1]
        elif max_y < position[1]:
            max_y = position[1]
    
    return ((min_x, max_x + 1), (min_y, max_y + 1))

def generate_chunk(
    game_map,
    game_map_chunk_mask,
    chunk_position):
    
    #check where surrounding chunks are
    #get their terrain information
    #draw based on what's around
    
    border_chunk_positions = set([(chunk_position[0], chunk_position[1] - 1),
                                  (chunk_position[0], chunk_position[1] + 1),
                                  (chunk_position[0] - 1, chunk_position[1]),
                                  (chunk_position[0] + 1, chunk_position[1])])
    
    touching_chunks = 0
    new_temp        = 0
    new_precip      = 0
    new_whatever    = 0
    for border_chunk in border_chunk_positions:
        if border_chunk in game_map_chunk_mask:
            touching_chunks += 1
            new_temp     += game_map_chunk_mask[border_chunk][0]
            new_precip   += game_map_chunk_mask[border_chunk][1]
            new_whatever += game_map_chunk_mask[border_chunk][2]
    
    #fill in based on surrounding chunks
    #the more touching chunks, the higher likelihood of randomizing
    
    if touching_chunks == 4:
        new_chunk = [
            new_temp     / 4,
            new_precip   / 4,
            new_whatever / 4]
    
    elif touching_chunks == 3:
        new_chunk = [
            new_temp     / 3,
            new_precip   / 3,
            new_whatever / 3]
        change_field = random.randint(0, 2)
        random_change = random.randint(0, 9)
        if random_change < 1:
            change = 0
            while change == 0:
                change = random.randint(-1, 1)
            new_value = new_chunk[change_field] + change
            if -4 <= new_value <= 4:
                new_chunk[change_field] = new_value
    
    elif touching_chunks == 2:
        new_chunk = [
            new_temp     / 2,
            new_precip   / 2,
            new_whatever / 2]
        change_field = random.randint(0, 2)
        random_change = random.randint(0, 10)
        if random_change < 3:
            change = 0
            while change == 0:
                change = random.randint(-1, 1)
            new_value = new_chunk[change_field] + change
            if -4 <= new_value <= 4:
                new_chunk[change_field] = new_value
    
    elif touching_chunks == 1:
        new_chunk = [
            new_temp    ,
            new_precip  ,
            new_whatever]
        change_field = random.randint(0, 2)
        random_change = random.randint(0, 10)
        if random_change < 5:
            change = 0
            while change == 0:
                change = random.randint(-1, 1)
            new_value = new_chunk[change_field] + change
            if -4 <= new_value <= 4:
                new_chunk[change_field] = new_value
    
    else:
        new_chunk = [0, 0, 0]
    
    game_map_chunk_mask[chunk_position] = tuple(new_chunk)
    
    game_map_chunk_bounds = (
        (chunk_position[0] * chunk_size,
         chunk_position[0] * chunk_size + chunk_size - 1),
        
        (chunk_position[1] * chunk_size,
         chunk_position[1] * chunk_size + chunk_size - 1)
        )
    
    for x in xrange(game_map_chunk_bounds[0][0], game_map_chunk_bounds[0][1] + 1):
        for y in xrange(game_map_chunk_bounds[1][0], game_map_chunk_bounds[1][1] + 1):
            new_tile = list(new_chunk)
            #perform micro-randomizations
            change_field = random.randint(0, 2)
            random_change = random.randint(0, 10)
            if random_change < 2:
                change = 0
                while change == 0:
                    change = random.randint(-1, 1)
                new_value = new_tile[change_field] + change
                if -4 <= new_value <= 4:
                    new_tile[change_field] = new_value
            
            for biome in biome_graph:
                if biome[0][0] <= new_tile[0] <= biome[0][1] and\
                   biome[1][0] <= new_tile[1] <= biome[1][1]:
                    tile_type = biome_graph[biome]
                    break
            #map values:
            #(('type', temp, precip, ??), [walkable, empty, see-through], items)
            game_map[x, y] = ((tile_type, new_tile[0], new_tile[1], new_tile[2]), [True, True, True], [])
    