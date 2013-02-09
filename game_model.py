#!/usr/bin/env python

import actor
import common
import item
import player
import terraform

class model(object):
    def __init__(self):
        # self.view = view
        self.run = True
        
        self.players = []
        self.actors = []
        
        self.landscape = None
        
        #current_actor is the actor who currently can act
        self.current_actor = None
        
        self.speed_lcm = None
        
        self.initialized = False
        
        self.add_actor('NULL', 'dog', 'NULL', 'human')
        
        self.human_actor = None
        
        self.level = None
    
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
        
        self.level = 1
        self.item_levels = [1, 2]
        
        self.generate_items()
        
        self.initialized = True
    
    
    ###################
    # string displays #
    ###################
    
    def print_actor(self):
        print self.current_actor
    
    ####################
    # items and actors #
    ####################
    
    def create_item(self, item_name, locs):
        self.landscape.landscape[locs][2].append(item.item(item_name))
    
    def remove_item(self, item_name, locs):
        self.landscape.landscape[locs][2].remove(item.item(item_name))
    
    def pick_up_item(self):
        item_list = self.landscape.landscape[self.current_actor.position][2]
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
            if self.is_location_walkable((x, y)):
                random_item = item.generate_random_with_chance(self.item_levels)
                if random_item != None:
                    self.landscape.landscape[x, y][2].append(random_item)
    
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
    
    def add_actor(self, name, actor_type, owner, owner_type, locs=None):
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
        
        new_actor = actor.actor(name, actor_type, owner, owner_type)
        new_actor.set_location((x, y))
        
        if name == 'NULL' and owner == 'NULL':
            self.current_actor = new_actor
            return
        
        self.landscape.landscape[x, y][1][1] = False
        
        # self.view.add_actor(new_actor)
        
        for i, each_player in enumerate(self.players):
            if each_player.name == owner:
                self.players[i].actors_owned.append(len(self.actors) - 1)
                break
        
        self.actors.append(new_actor)
        
        if self.initialized:
            for each_actor in self.actors[:-1]:
                each_actor.speed_time = float(each_actor.speed_time) / self.speed_lcm
            
            #scale old actor's speed times to new speed lcm
            self.speed_lcm = common.lcmm([each_actor.speed\
                                          for each_actor\
                                          in self.actors])
            for each_actor in self.actors[:-1]:
                each_actor.speed_time = int(each_actor.speed_time * self.speed_lcm)
            
            new_actor.speed_time = self.speed_lcm / new_actor.speed
    
    def remove_actor(self, remove_me):
        if remove_me in self.actors:
            self.actors.remove(remove_me)
    
    ##########################
    # modifying player/actor #
    ##########################
    
    def move_actor(self, direction):
        #direction is an integer of o'clock
        #since this is hexagonal, direction must be odd
        moved = False
        
        x, y = self.current_actor.position
        
        if y & 1 == 0:
            y_even = True
        else:
            y_even = False
        
        #diagonal up
        if direction == 1:
            if y_even:
                dx = 0
            else:
                dx = 1
            dy = -1
        elif direction == 11:
            if y_even:
                dx = -1
            else:
                dx = 0
            dy = -1
        
        #diagonal down
        elif direction == 5:
            if y_even:
                dx = 0
            else:
                dx = 1
            dy = 1
        elif direction == 7:
            if y_even:
                dx = -1
            else:
                dx = 0
            dy = 1
        
        #horizontal
        elif direction == 3:
            dx = 1
            dy = 0
        elif direction == 9:
            dx = -1
            dy = 0
        
        if (x + dx, y + dy) in self.landscape.landscape:
            #is walkable and is empty
            if self.landscape.landscape[x + dx, y + dy][1][0] == True and\
                self.landscape.landscape[x + dx, y + dy][1][1] == True:
                moved = True
        
        if moved:
            self.landscape.landscape[x, y][1][1] = True
            self.landscape.landscape[x + dx, y + dy][1][1] = False
            
            # self.view.move_actor_image(self.current_actor, x + dx, y + dy)
            
            self.current_actor.position = (x + dx, y + dy)
            
            self.next_turn()
            
            #check if centered actor has moved into a new chunk
            if self.current_actor == self.human_actor:
                chunk_size = terraform.chunk_size
                #check to generate new terrain
                #or check to delete out of range terrain
                if (x / chunk_size) != (x + dx / chunk_size) or\
                   (y / chunk_size) != (y + dy / chunk_size):
                    self.extend_map_from_actor(self.human_actor)
                    self.retract_map_from_actor(self.human_actor)
                    
                    #remove any actors that are now outside of viewing distance
                    for each_actor in self.actors:
                        if each_actor.position not in self.landscape.landscape:
                            self.remove_actor(each_actor)
        
        return moved
    
    def ai_action(self):
        #how unpythonic!
        if self.move_actor(9):
            pass
        elif self.move_actor(3):
            pass
    
    #############
    # map stuff #
    #############
    
    def extend_map_from_actor(self, extend_from_me):
        immediate_ungenerated_chunks = terraform.find_immediate_ungenerated(
            self.landscape,
            extend_from_me.position,
            terraform.check_chunk_generate_distance)
        
        if len(immediate_ungenerated_chunks) != 0:
            distant_ungenerated_chunks = terraform.find_immediate_ungenerated(
                self.landscape,
                extend_from_me.position,
                terraform.do_chunk_generate_distance)
            
            self.landscape.landscape_size = terraform.extend_map_using_ungenerated(
                self.landscape,
                distant_ungenerated_chunks)
    
    def retract_map_from_actor(self, retract_from_me):
        terraform.delete_map_at_position(
            self.landscape,
            retract_from_me.position)
    
    def is_location_walkable(self, locs):
        return self.landscape.landscape[locs][1][0] == True
    def is_location_empty(self, locs):
        return self.landscape.landscape[locs][1][1] == True
    def is_location_seethrough(self, locs):
        return self.landscape.landscape[locs][1][2] == True
    def is_location_interactable(self, locs):
        return self.landscape.landscape[locs][1][3] == True
    
    #################
    # updating view #
    #################
    
    # def set_background(self, new_background):
    #     self.view.background_map = new_background
    #     self.view.camera_x = None
    #     self.view.camera_y = None
    
    
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
        # for each_actor in self.actors:
        #     each_actor.update_chain(dt)
        
        if self.current_actor.owner_type == 'computer':
            self.ai_action()
