import actor
import common
import item
import player
import terraform
import copy
import ai
import random
import ability

class level(object):
    def __init__(self):
        self.level = None
        self.landscape = None
        self.actors = None
        self.human_actor_info = None

class model(object):
    def __init__(self, view):
        self.view = view
        self.run = True
        
        self.players = []
        self.actors = []
        
        self.actor_id_counter = 0
        
        #current_actor is the actor who currently can act
        self.current_actor = None
        
        self.speed_lcm = None
        
        self.initialized = False
        
        self.add_actor(self.actor_id_counter, 'NULL', 'dog', 'NULL', 'human')
        
        self.human_actor = None
        
        self.level = 1
        
        self.landscape = None
        self.stored_levels = []
        
    #############
    # true init #
    #############
    
    def initialize_map(self):
        #clear place holder actor
        del self.current_actor
        self.current_actor = None
        
        #set turn order
        self.speed_lcm = common.lcmm([each_actor.speed\
                                      for each_actor\
                                      in self.actors])
        
        for each_actor in self.actors:
            each_actor.speed_time = self.speed_lcm / each_actor.speed
            if self.current_actor == None:
                self.current_actor = each_actor
            elif each_actor.speed_time < self.current_actor.speed_time:
                self.current_actor = each_actor
            
            if each_actor.owner_type == 'human':
                self.human_actor = each_actor
        
        self.extend_map_from_actor(self.human_actor)
        
        self.item_levels = [1, 2]
        
        self.generate_items()
        
        self.view.landscape = self.landscape
        self.centered_actor = self.human_actor
        self.view.center_map(self.centered_actor)
        self.view.place_actors()
        
        self.view.initialize_interface()
        
        self.initialized = True
    
    ###################
    # string displays #
    ###################
    
    def print_actors(self):
        print 'model'
        for this_actor in self.actors:
            print this_actor
    
    def print_levels(self):
        for this_level in self.stored_levels:
            print 'Level: ' + str(this_level.level)
            print this_level.landscape
    
    def print_landscape_actors(self):
        self.landscape.print_actors()
    
    ####################
    # items and actors #
    ####################
    
    def create_item(self, item_name, locs):
        self.landscape.landscape[locs].items.append(item.item(item_name))
    
    def remove_item(self, item_name, locs):
        self.landscape.landscape[locs].items.remove(item.item(item_name))
    
    def pick_up_item(self):
        item_list = self.landscape.landscape[self.current_actor.position].items
        if len(item_list) > 0:
            this_item = item_list[0]
            self.current_actor.add_item(this_item)
            item_list.remove(this_item)
    
    def give_item_to_actor(self, this_actor, add_item):
        if type(add_item) == str:
            add_item = item.item(add_item)
        this_actor.add_item(add_item)
    
    def generate_items(self):
        for x, y in self.landscape.landscape:
            if self.landscape.landscape[x, y].walkable:
                random_item = item.generate_random_with_chance(self.item_levels)
                if random_item != None:
                    self.landscape.landscape[x, y].items.append(random_item)
    
    ##################################
    # adding/removing players/actors #
    ##################################
    
    def add_player(self, name, player_type):
        #name:
        #name of player
        
        #player_type:
        #'human', or 'computer'
        new_player = player.player(name, player_type)
        self.players.append(new_player)
    
    def add_actor(self, id_number, name, actor_type, owner, owner_type, locs=None):
        self.actor_id_counter += 1
        #name:
        #name of actor
        
        #actor_type:
        #'dog', 'cat', etc...
        
        #owner:
        #name of player
        
        #x, y:
        #coordinates on map, NOT pixel coordinates on screen
        
        if locs == None:
            x, y = None, None
        else:
            x, y = locs
        
        new_actor = actor.actor(id_number, name, actor_type, owner, owner_type)
        new_actor.set_location((x, y))
        
        if name == 'NULL' and owner == 'NULL':
            self.current_actor = new_actor
            return
        
        self.landscape.landscape[x, y].occupied = True
        self.landscape.landscape[x, y].actors.append(new_actor)
        
        self.view.add_actor(new_actor)
        
        for i, each_player in enumerate(self.players):
            if each_player.name == owner:
                self.players[i].actors_owned.append(len(self.actors) - 1)
                break
        
        self.actors.append(new_actor)
        
        if self.initialized:
            self.recalculate_speed()
            
            new_actor.speed_time = self.speed_lcm / new_actor.speed
    
    def remove_actor(self, remove_me):
        if remove_me in self.actors:
            self.actors.remove(remove_me)
    
    def remove_actor_by_id(self, remove_me):
        for each_actor in self.actors:
            if each_actor.id_number == remove_me:
                break
        self.actors.remove(each_actor)
    
    def recalculate_speed(self):
        for each_actor in self.actors[:-1]:
            each_actor.speed_time = float(each_actor.speed_time) / self.speed_lcm
        
        #scale old actor's speed times to new speed lcm
        self.speed_lcm = common.lcmm([each_actor.speed\
                                      for each_actor\
                                      in self.actors])
        for each_actor in self.actors[:-1]:
            each_actor.speed_time = int(each_actor.speed_time * self.speed_lcm)
    
    def remove_actor(self, remove_me):
        #remove from tile and model actor list
        self.remove_actor_by_id(remove_me.id_number)
        
        #map may have shrank after actor went off map
        if remove_me.position in self.landscape.landscape:
            self.landscape.landscape[remove_me.position].occupied = False
            self.landscape.landscape[remove_me.position].actors.pop()
        
        #remove from view
        self.view.remove_actor(remove_me)
    
    ##########################
    # modifying player/actor #
    ##########################
    
    def move_actor(self, direction):
        #direction is an integer of o'clock
        #since this is hexagonal, direction must be odd
        x, y = self.current_actor.position
        
        dx, dy = common.get_coordinates_offset_from_direction((x, y), direction)
        
        moved = False
        
        if dx == dy == 0:
            #pausing
            moved = True
        
        elif (x + dx, y + dy) in self.landscape.landscape:
            #is walkable and is empty
            if self.landscape.landscape[x + dx, y + dy].walkable == True and\
                self.landscape.landscape[x + dx, y + dy].occupied == False:
                moved = True
        
        if moved:
            self.landscape.landscape[x, y].occupied = False
            self.landscape.remove_actor(self.current_actor.id_number)
            self.landscape.landscape[x + dx, y + dy].occupied = True
            self.landscape.landscape[x + dx, y + dy].actors.append(self.current_actor)
            
            old_position = (x, y)
            self.current_actor.old_position = old_position
            self.current_actor.position = (x + dx, y + dy)
            
            ###################################################
            # check if human actor has moved into a new chunk #
            ###################################################
            
            map_changed = False
            old_map_bounds = self.landscape.landscape_size
            
            if self.current_actor == self.human_actor:
                chunk_size = terraform.chunk_size
                #check to generate new terrain
                #or check to delete out of range terrain
                if int(x / chunk_size) != int((x + dx) / chunk_size) or\
                   int(y / chunk_size) != int((y + dy) / chunk_size):
                    map_changed = self.do_full_extension_retraction()
            
            ###############
            # update view #
            ###############
            
            if direction != -1:
                self.current_actor.change_direction(direction)
            
            if map_changed:
                #shift tile offset (which as a result shifts everything else)
                new_map_bounds = self.landscape.landscape_size
                screen_change_direction = self.view.screen_offset_from_map_direction(old_map_bounds, new_map_bounds)
                self.view.shift_tile_offset(screen_change_direction)
            
            
            
            self.view.move_actor_image(self.current_actor)
            
            self.next_turn()
        
        return moved
    
    ###################
    # actor abilities #
    ###################
    
    def add_ability(self, actor, number_slot, ability_object):
        #modify actor
        actor.add_ability(number_slot, ability_object)
        
        #modify view
        self.view.add_ability(number_slot, ability_object)
    
    def remove_ability(self, number_slot):
        #modify actor
        actor.remove_ability(number_slot)
        
        #modify view
        self.view.remove_ability(number_slot)
    
    def use_ability(self, direction, ability):
        offset_coordinates = common.get_coordinates_offset_from_direction(self.human_actor.position, direction)
        target_coordinates = (self.human_actor.position[0] + offset_coordinates[0],
                              self.human_actor.position[1] + offset_coordinates[1])
        target_tile = self.landscape.landscape[target_coordinates]
        if target_tile.occupied:
            damage_modifier = ability.modifiers['damage_modifier']
            damage = -self.human_actor.make_damage(modifier=damage_modifier)
            target_actor = target_tile.actors[0]
            target_actor.modify_health(damage)
            
            if target_actor.current_health <= 0:
                self.remove_actor(target_actor)
            
            self.next_turn()
            return True
        else:
            return False
    
    def ai_action(self):
        #consider that there may be special actions an ai can do:
        #1. running away from a time bomb
        #2. setting a trap
        #3. etc
        
        current_actor_ai = self.current_actor.ai
        
        current_actor_position = self.current_actor.position
        target_actor_position = self.current_actor.ai.target.position
        distance_to_target = common.hex_distance(current_actor_position, target_actor_position)
        
        current_actor_running_distance = current_actor_ai.behavior_running_distance
        
        path_to_target = self.landscape.pathfind(current_actor_position, target_actor_position)
        
        distance_check = current_actor_ai.is_distance_in_running(distance_to_target)
        
        def stand_still():
            self.move_actor(-1)
        
        def proceed():
            move_to_position = path_to_target[1]
            direction = common.get_direction(current_actor_position, move_to_position)
            self.move_actor(direction)
        
        def run_away():
            move_to_position = path_to_target[1]
            direction = common.get_direction(current_actor_position, move_to_position)
            inverted_direction = common.invert_oclock(direction)
            side_step = [-2, 2]
            random.shuffle(side_step)
            if self.move_actor(inverted_direction):
                pass
            elif self.move_actor(inverted_direction + side_step[0]):
                pass
            elif self.move_actor(inverted_direction - side_step[1]):
                pass
            else:
                self.move_actor(-1)
        
        #resting, unaware of anything to attack.
        if current_actor_ai.is_mood_resting():
            self.move_actor(-1)
        
        #normal, aware of something to attack.
        elif current_actor_ai.is_mood_normal():
            if current_actor_ai.is_behavior_chaser():
                if distance_check == 0 or distance_check == -1:
                    stand_still()
                else:
                    proceed()
        
            elif current_actor_ai.is_behavior_runner():
                if distance_check == -1:
                    run_away()
                elif distance_check == 0:
                    stand_still()
                else:
                    proceed()
        
        #afraid, run away
        elif current_actor_ai.is_mood_afraid():
            run_away()
        
        #berserk, chase
        elif current_actor_ai.is_mood_berserk():
            if distance_to_target == 1:
                stand_still()
            else:
                proceed()
    
    #############
    # map stuff #
    #############
    
    def do_full_extension_retraction(self):
        #retract before extending!
        retract_changed = self.retract_map_from_actor(self.human_actor)
        extend_changed = self.extend_map_from_actor(self.human_actor)
        
        changed = retract_changed or extend_changed
        
        #remove any actors that are now outside of viewing distance
        remove_indeces = []
        for i, each_actor in enumerate(self.actors):
            if not self.landscape.has_actor(each_actor):
                remove_indeces.append(i)
                self.view.remove_actor(each_actor)
        
        #add to list to avoid changing self.actors while looping through it
        while len(remove_indeces) > 0:
            self.remove_actor(self.actors[remove_indeces[0]])
            remove_indeces.pop(0)
        
        return changed
    
    def extend_map_from_actor(self, extend_from_me):
        immediate_ungenerated_chunks = terraform.find_immediate_ungenerated(
            self.landscape,
            extend_from_me.position,
            terraform.check_chunk_generate_distance)
        
        extended = False
        
        if len(immediate_ungenerated_chunks) != 0:
            distant_ungenerated_chunks = terraform.find_immediate_ungenerated(
                self.landscape,
                extend_from_me.position,
                terraform.do_chunk_generate_distance)
            
            self.landscape.landscape_size = terraform.extend_map_using_ungenerated(
                self.landscape,
                distant_ungenerated_chunks)
            
            extended = True
        
        return extended
    
    def retract_map_from_actor(self, retract_from_me):
        return terraform.delete_map_at_position(
            self.landscape,
            retract_from_me.position)
    
    def traverse_portal(self):
        direction = self.landscape.get_portal_direction_at_location(self.human_actor.position)
        if direction == None:
            return False
        
        self.landscape.traversed_location = self.human_actor.position
        
        if direction == 'up':
            if self.level - 1 == len(self.stored_levels):
                #store old
                self.stored_levels.append(self.store_level())
                
                self.level += 1
                
                #generate new level
                self.landscape = terraform.make_terrain_test(str(self.level) + '_grass')
                
                self.actors = [self.human_actor]
                
                #set actor's position in new world (modify internal data of new landscape)
                self.human_actor.position = (0, 0)
                self.landscape.landscape[0, 0].occupied = True
                self.landscape.landscape[0, 0].actors.append(self.human_actor)
                                
                #generate map
                self.do_full_extension_retraction()
                
                #make new speed lcm
                self.recalculate_speed()
            
            else:
                #store current level over old level
                self.stored_levels.pop(self.level - 1)
                this_level = self.store_level()
                self.stored_levels.insert(self.level - 1, this_level)
                
                self.level += 1
                
                #load old level
                self.load_level(self.level - 1)
        
        elif direction == 'down':
            #if this is the top level, save it new and insert at end
            if len(self.stored_levels) == self.level - 1:
                this_level = self.store_level()
                self.stored_levels.append(this_level)
            
            else:
                #store current level over old level
                self.stored_levels.pop(self.level - 1)
                
                this_level = self.store_level()
                self.stored_levels.insert(self.level - 1, this_level)
            
            self.level -= 1
            self.load_level(self.level - 1)
        
        return True
    
    #########################
    # level storing/loading #
    #########################
    
    def store_level(self):
        this_level = level()
        this_level.level = self.level
        
        this_level.landscape = copy.deepcopy(self.landscape)
        
        #remove human actor from stored landscape
        this_level.landscape.remove_actor(self.human_actor.id_number)
        
        #do not save human directly
        for each_actor in self.actors:
            if each_actor.id_number == self.human_actor.id_number:
                break
        self.actors.remove(each_actor)
        this_level.actors = copy.deepcopy(self.actors)
        
        this_level.human_actor_info = {}
        this_level.human_actor_info['speed_time'] = self.human_actor.speed_time
        this_level.human_actor_info['pos'] = self.human_actor.position
        return this_level
    
    def load_level(self, number):
        next_level = self.stored_levels[number]
        
        self.landscape = next_level.landscape
        self.actors = next_level.actors
        
        #re-append human actor to actor list
        self.actors.append(self.human_actor)
        
        self.human_actor.speed_time = next_level.human_actor_info['speed_time']
        self.human_actor.position = next_level.human_actor_info['pos']
        
        #re-append human actor to landscape tile
        human_tile = self.landscape.landscape[self.human_actor.position]
        human_tile.actors.append(self.human_actor)
        
        self.recalculate_speed()
    
    #################
    # updating view #
    #################
    
    def set_background(self, new_background):
        self.view.background_map = new_background
        self.view.camera_x = None
        self.view.camera_y = None
    
    ##################
    # updating model #
    ##################
    
    def next_turn(self):
        current_actor = self.current_actor
        min_speed = current_actor.speed_time
        
        for each_actor in self.actors:
            each_actor.speed_time -= min_speed
        current_actor.speed_time += (self.speed_lcm / current_actor.speed)
        
        self.current_actor = None
        for each_actor in self.actors:
            if self.current_actor == None:
                self.current_actor = each_actor
            elif each_actor.speed_time < self.current_actor.speed_time:
                self.current_actor = each_actor
    
    def quit(self):
        self.run = False
    
    def update(self, dt):
        if self.current_actor.owner_type == 'computer':
            if self.current_actor.ai.target != None:
                self.ai_action()
            elif self.move_actor(9):
                pass
            elif self.move_actor(3):
                pass

