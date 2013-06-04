import random
import common

#(0, 0)        (1, 0)        (2, 0)
#       (0, 1)        (1, 1)        (2, 1)
#(0, 2)        (1, 2)        (2, 2)


#########

#all chunks within this many distance units from the human must be
#generated whenever a generation is requested
#testing: 30 chunks
do_chunk_generate_distance = 3

#when a deletion is requested, chunks within this many distance units
#from the human must be deleted
do_chunk_delete_distance = 3

#a generation is requested when the human is within this many
#chunks from the edge of the world.
#when the human reaches the boundary of this region,
#another check for land is made. if that request can be carried out,
#it will.
#testing: 12 chunks
check_chunk_generate_distance = 3

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

#to do: make this a subclass of a pygame sprite to make use of its rect
#and image field when drawing the map. it would make animations easier, and,
#more importantly, possible
class tile(object):
    def __init__(self, information=None):
        if information != None:
            self.write(information)
        else:
            self.temperature = None
            self.precipitation = None
            self.psych = None
            
            self.terrain_image_name = None
            
            self.terrain_type = None
            
            self.walkable = None
            self.occupied = None
            self.seethrough = None
            self.interactable = None
            
            self.items = []
        
        self.actors = []
    
    def write(self, information):
        self.temperature = information[0][0]
        self.precipitation = information[0][1]
        self.psych = information[0][2]
        
        for biome in biome_graph:
            if biome[0][0] <= self.temperature <= biome[0][1] and\
               biome[1][0] <= self.temperature <= biome[1][1]:
                self.terrain_type = biome_graph[biome]
                break
        
        self.walkable     = information[1][0]
        self.occupied     = information[1][1]
        self.seethrough   = information[1][2]
        self.interactable = information[1][3]
        
        self.items = information[2]
        
        self.images = information[3]

class landscape(object):
    def __init__(self, level):
        self.landscape = {}
        self.landscape_chunk_mask = {}
        self.landscape_size = None
        
        self.cities = []
        
        self.portals = []
        self.level = level
        #traversed_location is where the player entered a portal
        self.traversed_location = None
    
    #center is actor to center map on. accounts for sight of actor.
    def __str__(self, center_actor=None):
        if center_actor != None:
            #get tiles in sight distance of center_actor
            
            center_actor_position = center_actor.position
            
            print_me = ''
            for y in xrange(self.landscape_size[1][0], self.landscape_size[1][1]):
                if y & 1 == 1:
                    print_me += ' '
                for x in xrange(self.landscape_size[0][0], self.landscape_size[0][1]):
                    chunk_location = (int(x / chunk_size), int(y / chunk_size))
                    distance_to_actor = common.hex_distance(center_actor_position, (x, y))
                    if distance_to_actor <= center_actor.sight_distance:
                        if self.get_portal_direction_at_location((x, y)) != None:
                            print_me += self.get_portal_direction_at_location((x, y))[0] + ' '
                        elif self.location_has_building((x, y)):
                            print_me += 'b '
                        elif self.chunk_in_city_bounds((chunk_location)):
                            print_me += 'c '
                        elif self.landscape[x, y].occupied:
                            print_me += 'a '
                        else:
                            print_me += '. '
                    else:
                        print_me += '  '
                print_me += '\n'
            print_me += '\n'
        else:
            print_me = ''
            for y in xrange(self.landscape_size[1][0], self.landscape_size[1][1]):
                if y & 1 == 1:
                    print_me += ' '
                for x in xrange(self.landscape_size[0][0], self.landscape_size[0][1]):
                    chunk_location = (int(x / chunk_size), int(y / chunk_size))
                    if self.get_portal_direction_at_location((x, y)) != None:
                        print_me += self.get_portal_direction_at_location((x, y))[0] + ' '
                    elif self.location_has_building((x, y)):
                        print_me += 'b '
                    elif self.chunk_in_city_bounds((chunk_location)):
                        print_me += 'c '
                    elif self.landscape[x, y].occupied:
                        print_me += 'a '
                    else:
                        print_me += '. '
                print_me += '\n'
            print_me += '\n'
        return print_me
    
    def __repr__(self):
        return self.landscape.__str__()
    
    def chunk_in_city_bounds(self, this_chunk):
        for this_city in self.cities:
            if this_chunk in this_city.chunk_locations:
                return True
        return False
    
    def location_has_building(self, this_location):
        this_chunk = (int(this_location[0] / chunk_size), int(this_location[1] / chunk_size))
        for this_city in self.cities:
            if this_chunk in this_city.chunk_locations:
                for this_building in this_city.buildings:
                    if this_building.location == this_location:
                        return True
        return False
    
    def get_portal_direction_at_location(self, location):
        for this_portal in self.portals:
            if this_portal.location == location:
                return this_portal.direction
        return None
    
    def has_actor(self, this_actor):
        for this_tile in self.landscape:
            if this_actor in self.landscape[this_tile].actors:
                return True
        return False
    
    def print_actors(self):
        print 'land'
        for this_tile in self.landscape:
            for this_actor in self.landscape[this_tile].actors:
                print this_tile
                print this_actor
    
    def remove_actor(self, actor_id):
        do_remove = False
        for location in self.landscape:
            for each_actor in self.landscape[location].actors:
                if each_actor.id_number == actor_id:
                    do_remove = True
                    break
            if do_remove:
                self.landscape[location].actors.remove(each_actor)
                break
    
    ###################################
    # pathfinding and related goodies #
    ###################################
    
    def is_open_path(p0, p1):
        #if a path is found from p0 to p1 that is equal to the distance of the
        #points, then there is an open path.
        return len(self.pathfind(p0, p1)) - 1 == common.hex_distance(p0, p1)
    
    #a* based
    def pathfind(self, p0, p1):
        open_list = [p0]
        closed_list = []
        
        closed_list.append(p0)
        
        current_point = p0
        
        current_path = []
        
        while len(open_list) != 0:
            closed_list.append(current_point)
            
            adjacent_points = common.get_adjacent(current_point)
            #append adjacent points that aren't in open
            for adjacent_point in adjacent_points:
                if adjacent_point not in closed_list and\
                        not self.landscape[adjacent_point].occupied and\
                        self.landscape[adjacent_point].walkable or\
                        adjacent_point == p1:
                    open_list.append(adjacent_point)
            
            #get best f of adjacent
            best_f = None
            best_adjacent = None
            for adjacent_point in adjacent_points:
                if adjacent_point in open_list:
                    f_score = common.hex_distance(adjacent_point, p1)
                    if best_f == None or f_score < best_f:
                        best_f = f_score
                        best_adjacent = adjacent_point
            
            if best_f == None:
                if len(current_path) == 0:
                    #not possible to find path
                    path_found = False
                    break
                else:
                    closed_list.append(current_point)
                    current_point = current_path[-1]
            elif best_adjacent == p1:
                current_path.append(current_point)
                path_found = True
                break
            else:
                #one more point towards the end (hopefully)
                current_path.append(current_point)
                current_point = best_adjacent
        
        if path_found:
            current_path.append(p1)
            return current_path
        else:
            return []

#each city has 3-4 (or more?) chunks designated to its boundaries.
#its building placements are stored. its terrain is not stored.
#building types: civilian (questing), item shop, trainers (each city has 
#1-2 trainer types for skills (fighting/blocking/healing))
class city(object):
    def __init__(self, chunk_locations):
        #chunk_location is in format: ((x, y), (x, y), (x, y)...)
        self.chunk_locations = chunk_locations
        self.buildings = []

building_type_list = ['civilian', 'item', 'instructor']
class building(object):
    def __init__(self, location):
        self.civilian_list = []
        self.item_list = []
        self.instructor_list = []
        
        self.this_type = None
        
        self.location = location
    
    def populate(self, this_type=None):
        #if this_type is None, a random city actor type is given.
        #else, it will use that type
        if this_type == None:
            building_type = building_type_list[random.randint(0, 2)]
        else:
            building_type = this_type

class portal(object):
    def __init__(self, location, direction):
        self.location = location
        self.direction = direction

def make_terrain_test(scheme):
    #10x15 map
    if scheme == 'basic_grass':
        this_landscape = landscape(1)
        this_landscape.landscape_size = ((0, 5), (0, 5))
        for x in xrange(5):
            for y in xrange(5):
                this_tile = tile(((0, 0, 0), [True, False, True, False], [], []))
                this_landscape.landscape[x, y] = this_tile
        for x in xrange(1):
            for y in xrange(1):
                this_landscape.landscape_chunk_mask[x, y] = (0, 0, 0)
        
        #generate 2 cities: in range, and out of range
        add_this_city = city(((1, 1), (2, 1), (1, 2), (2, 2)))
        
        add_this_building = building((5, 5))
        add_this_building.populate('civilian')
        add_this_city.buildings.append(add_this_building)
        
        add_this_building = building((6, 5))
        add_this_building.populate('item')
        add_this_city.buildings.append(add_this_building)
        
        add_this_building = building((7, 5))
        add_this_building.populate('instructor')
        add_this_city.buildings.append(add_this_building)
        
        this_landscape.cities.append(add_this_city)
        
        add_this_city = city(((-4, 1), (-4, 0), (-5, 1), (-5, 0)))
        
        add_this_building = building((-20, 0))
        add_this_building.populate('civilian')
        add_this_city.buildings.append(add_this_building)
        
        add_this_building = building((-19, 0))
        add_this_building.populate('item')
        add_this_city.buildings.append(add_this_building)
        
        add_this_building = building((-18, 0))
        add_this_building.populate('instructor')
        add_this_city.buildings.append(add_this_building)
        
        this_landscape.cities.append(add_this_city)
        
        add_this_portal = portal((2, 0), 'up')
        this_landscape.portals.append(add_this_portal)
        
        return this_landscape

#get ungenerated in given distance
def find_immediate_ungenerated(
    this_landscape,
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
    generated_chunks = set(this_landscape.landscape_chunk_mask.keys())
    
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
    this_landscape,
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
                if border_chunk in this_landscape.landscape_chunk_mask:
                    bordering += 1
            if 4 >= bordering >= generate_for_touch:
                touching_threshold.append(ungenerated_chunk)
        
        for ungenerated_chunk in touching_threshold:
            generate_chunk(
                this_landscape,
                ungenerated_chunk)
            ungenerated_chunks.remove(ungenerated_chunk)
        
        if len(touching_threshold) == 0:
            generate_for_touch -= 1
        else:
            generate_for_touch = 4
    
    min_x = this_landscape.landscape.keys()[0][0]
    max_x = this_landscape.landscape.keys()[0][0]
    min_y = this_landscape.landscape.keys()[0][1]
    max_y = this_landscape.landscape.keys()[0][1]
    
    for position in this_landscape.landscape.keys():
        if min_x > position[0]:
            min_x = position[0]
        
        if max_x < position[0]:
            max_x = position[0]
        
        if min_y > position[1]:
            min_y = position[1]
        
        if max_y < position[1]:
            max_y = position[1]
    
    return ((min_x, max_x + 1), (min_y, max_y + 1))

#assumes actor's position, not in chunk form
def delete_map_at_position(
    this_landscape,
    position):
    
    chunk_position = (int(position[0] / chunk_size), int(position[1] / chunk_size))
    
    safe_chunk_positions = []
    for x_position in xrange(chunk_position[0] - do_chunk_delete_distance, chunk_position[0] + do_chunk_generate_distance + 1):
        for y_position in xrange(chunk_position[1] - do_chunk_delete_distance, chunk_position[1] + do_chunk_generate_distance + 1):
            safe_chunk_positions.append((x_position, y_position))
    
    retract_changed = False
    
    for map_position in this_landscape.landscape.keys():
        if (int(map_position[0] / chunk_size), int(map_position[1] / chunk_size)) not in safe_chunk_positions:
            del this_landscape.landscape[map_position]
            retract_changed = True
    for chunk_position in this_landscape.landscape_chunk_mask.keys():
        if chunk_position not in safe_chunk_positions:
            del this_landscape.landscape_chunk_mask[chunk_position]
    
    return retract_changed

def generate_chunk(
    this_landscape,
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
        if border_chunk in this_landscape.landscape_chunk_mask:
            touching_chunks += 1
            new_temp     += this_landscape.landscape_chunk_mask[border_chunk][0]
            new_precip   += this_landscape.landscape_chunk_mask[border_chunk][1]
            new_whatever += this_landscape.landscape_chunk_mask[border_chunk][2]
    
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
    
    this_landscape.landscape_chunk_mask[chunk_position] = tuple(new_chunk)
    
    this_landscape.landscape_chunk_bounds = (
        (chunk_position[0] * chunk_size,
         chunk_position[0] * chunk_size + chunk_size - 1),
        
        (chunk_position[1] * chunk_size,
         chunk_position[1] * chunk_size + chunk_size - 1)
        )
    
    for x in xrange(this_landscape.landscape_chunk_bounds[0][0], this_landscape.landscape_chunk_bounds[0][1] + 1):
        for y in xrange(this_landscape.landscape_chunk_bounds[1][0], this_landscape.landscape_chunk_bounds[1][1] + 1):
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
            
            #map values:
            #(
            #('type', temp, precip, ??),
            #[walkable, empty, see-through, interactable],
            #[items],
            #[images in order of layering]
            #)
            this_landscape.landscape[x, y] = tile(((new_tile[0], new_tile[1], new_tile[2]), [True, False, True, False], [], []))
    
    #post processing to add land features (cities, doodads, etc)
    
