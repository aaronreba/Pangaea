from __future__ import division

import pygame
from math import sqrt
from math import ceil

import random

import common

import ai

MS_PER_FRAME = 100

class actor(pygame.sprite.Sprite):
    def __init__(self, id_number, name, actor_type, owner, owner_type):
        self.id_number = id_number
        
        #name: name of actor
        #actor_type: 'dog, 'cat', etc...
        #owner: name of player
        #owner_type: 'human', 'computer'
        
        self.name = name
        self.actor_type = actor_type
        self.owner = owner
        self.owner_type = owner_type
        
        #position on map
        self.position = None
        
        #how far actor can see
        self.sight_distance = 5
        
        #########
        # stats #
        #########
        
        self.stats = {}
        
        #4 base stats:
        #offense
        #health
        #whatever the fuck agility does (crit?)
        #defense
        self.stats['power']     = 1000
        self.stats['agility']   = 10
        self.stats['vitality']  = 10
        self.stats['toughness'] = 10
        
        self.stats['health'] = 70
        self.stats['mana']   = 30
        
        #lucky stats
        self.stats['evasion'] = 0
        self.stats['crit']    = 0
        
        #speed is how often actor moves
        self.speed = 100
        self.speed_time = None
        
        self.current_health = self.stats['health']
        
        ############
        # statuses #
        ############
        
        self.statuses = {}
        
        #########
        # items #
        #########
        
        self.inventory = []
        self.gold = 0
        
        #keep equipment simple
        self.equipment = {}
        
        self.equipment['left_hand']  = None
        self.equipment['right_hand'] = None
        
        self.equipment['head']  = None
        self.equipment['chest'] = None
        self.equipment['legs']  = None
        self.equipment['hands'] = None
        self.equipment['feet']  = None
        
        self.equipment['neck'] = None
        
        ##########
        # skills #
        ##########
        
        self.skills = {}
        
        ######
        # ai #
        ######
        
        #for humans, ai is only a storage structure.
        #if the player is berserk, it can't use complex attacks (only direct attacks).
        #if the player is scared, it can't attack.
        self.ai = ai.ai()
        
        ##########################
        # view/sprite attributes #
        ##########################
        
        self.destination = None
        
        #the path the actor will take to get to the destination
        self.current_path = []
        
        #chains hold frames
        #an entry is like so:
        #image_chains[act] = [image, ]
        self.image_chains = None
        
        self.rect = None #inherited from Sprite, position on screen
        self.image = None #inherited from Sprite
        
        self.decimal_rect = (0, 0) #holds decimals that pygame's rect destroys
        
        # self.visible = False
        
        #this is for the view displaying something walking
        self.walking_speed = 200 #value in pixels
        self.walking_destination = (0, 0)
        self.walking_vector = (0, 0)
        
        #starting direction
        self.facing_direction = 5
        
        #tuple of (True, False). True = positive direction, False = negative
        self.walking_direction_boolean = None
    
    def __str__(self):
        inventory_string = ' '.join([x.name for x in self.inventory])
        equipment_string = ''
        for equipment in self.equipment:
            if self.equipment[equipment] == None:
                equipment_string += 'None '
            else:
                equipment_string += self.equipment[equipment].name + ' '
        
        return\
'id: {9}\n\
health: {10}/{0}, mana: {1}\n\
power: {2}, toughness: {3}, agility: {4}, vitality: {5}\n\
inventory: {6}\n\
equipment: {7}\n\
position: {8}'.format(
            self.stats['health'],
            self.stats['mana'],
            self.stats['power'],
            self.stats['toughness'],
            self.stats['agility'],
            self.stats['vitality'],
            inventory_string,
            equipment_string,
            str(self.position),
            str(self.id_number),
            self.current_health)
    
    def __eq__(self, other):
        if type(self) == type(other):
            return self.id_number == other.id_number
        else:
            return False
    
    def equip_item(self, item):
        #return_item is a list of whatever items that were
        #removed in order to equip the given item
        return_items = [None]
        if item.location == '1hand':
            if self.equipment['right_hand'] == None:
                self.equipment['right_hand'] = item
            
            elif self.equipment['right_hand'].location == '2hand':
                return_items = [self.unequip_item_at_location['right_hand']]
                self.equipment['right_hand'] = item
            
            elif self.equipment['left_hand'] == None:
                self.equipment['left_hand'] = item
            
            else:
                return_items = [self.unequip_item_at_location['right_hand']]
                self.equipment['right_hand'] = item
        
        elif item.location == '2hand':
            return_items = [self.unequip_item_at_location('right_hand'),
                            self.unequip_item_at_location('left_hand')]
            
            self.equipment['right_hand'] = item
        
        else:
            return_items = [self.unequip_item_at_location(item.location)]
            
            self.equipment[item.location] = item
        
        for stat in item.stats:
            self.stats[stat] += item.stats[stat]
        
        self.recalculate_health()
        
        for return_item in return_items:
            self.add_item(return_item)
    
    def unequip_item(self, item):
        self.equipment[item.location] = None
        
        for stat in item.stats:
            self.stats[stat] -= item.stats[stat]
        
        self.recalculate_health()
        
        return item
    
    def unequip_item_at_location(self, location):
        location_item = self.equipment[location]
        if location_item != None:
            self.unequip_item(location_item)
            for stat in location_item.stats:
                self.stats[stat] -= location_item.stats[stat]
            
            self.recalculate_health()
        return location_item
    
    def has_item_at_location(self, location):
        return self.equipment[location] == None
    
    def add_item(self, item):
        if item != None and len(self.inventory) < 30:
            self.inventory.append(item)
    
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
    
    def recalculate_health(self):
        self.stats['health'] = self.stats['vitality'] * 7
    
    def add_gold(self, gold):
        self.gold += gold
    
    def remove_gold(self, gold):
        self.gold -= gold
    
    def modify_health(self, amount):
        #returns false on death
        #returns true otherwise
        self.current_health += amount
        if self.current_health < 0:
            return False
        elif self.current_health > self.stats['health']:
            self.current_health = self.stats['health']
        return True
    
    def make_damage(self, modifier=1.0, cone=10.0):
        damage_value = self.stats['power'] * modifier
        random_max = damage_value * cone
        random_modifier = random.uniform(-random_max, random_max)
        damage_value += random_modifier
        damage_value = round(damage_value)
        return int(damage_value)
    
    def initialize_sprite(self, group):
        pygame.sprite.Sprite.__init__(self, group)
    
    def initialize_animation(self, image_chains):
        self.image_chains = image_chains
        self.current_act = 'stand'
        self.current_act_animation_index = 0
        self.current_act_frame_index = 0
        self.current_act_frame = self.image_chains['stand'][self.facing_direction][0]
        self.current_act_number_of_animations = len(self.image_chains['stand'][self.facing_direction])
        self.current_act_animation_length = len(self.image_chains['stand'][self.facing_direction][0])
        self.current_act_time = 0
        self.current_act_alotted_time = MS_PER_FRAME
    
    def change_act(self, new_act):
        action_list = ['stand', 'walk']
        action_list.index(new_act)
      
        if self.current_act == new_act:
            return
        
        
        old_act = self.current_act
      
        self.current_act = new_act
        self.current_act_animation_index = 0
        self.current_act_frame_index = 0
        self.current_act_frame = self.image_chains[new_act][self.facing_direction][0]
        self.current_act_number_of_animations = len(self.image_chains[new_act][self.facing_direction])
        self.current_act_animation_length = len(self.image_chains[new_act][self.facing_direction][0])
        self.current_act_time = 0
        self.current_act_alotted_time = MS_PER_FRAME
      
        if new_act == 'walk':
            self.decimal_rect = [0, 0]
      
    def change_direction(self, new_direction):
        self.facing_direction = new_direction
    
    def set_walk(self, new_location=None):
        #set walk to SCREEN COORDINATES
        current_actor_coordinates = (self.rect[0] + self.decimal_rect[0],
                                     self.rect[1] + self.decimal_rect[1])
        if new_location == None:
            new_location = self.walking_destination
        
        move_x = new_location[0] - current_actor_coordinates[0]
        move_y = new_location[1] - current_actor_coordinates[1]
        
        self.walking_destination = new_location
        self.walking_destination = (int(self.walking_destination[0]),
                                    int(self.walking_destination[1]))
        
        self.walking_vector = common.vector_to_pos(current_actor_coordinates,
                                                   new_location,
                                                   self.walking_speed)
        
        if self.walking_vector[0] > 0:
            bx = True
        else:
            bx = False
        if self.walking_vector[1] > 0:
            by = True
        else:
            by = False
        
        self.walking_direction_boolean = (bx, by)
    
    def set_location(self, (x, y)):
        self.position = (x, y)
        
    def add_destination(self, x, y):
        self.destination = (x, y)
    
    #def load_images(self, images):
    #    #if image set is not loaded yet, load it
    #    if self.actor_type not in images.images:
    #        images.images.load_images(self.actor_type)
    #    
    #    #image set is now loaded whether or not it was found.
    #    #now reference it.
    #    self.image_chains = images.images[self.actor_type]
    #deprecated: now handled by model
    
    def update_chain(self, dt):
        #todo: this may be INCREDIBLY slow later on with many actors
      
        self.current_act_time += dt
        #using while loop in case of skipped frames
      
        #do... add dt to current act time, if it passes the time of the frame,
        #increment or loop around index, change frame, and set frame chain
      
        while self.current_act_time >= self.current_act_alotted_time:
            self.current_act_time -= self.current_act_alotted_time
            self.current_act_frame_index += 1
            if self.current_act_frame_index == self.current_act_animation_length:
                self.current_act_animation_index = random.randint(0, self.current_act_number_of_animations - 1)
                self.current_act_frame_index = 0
        self.image = self.image_chains[self.current_act]\
                                      [self.facing_direction]\
                                      [self.current_act_animation_index]\
                                      [self.current_act_frame_index]
      
        if self.current_act == 'walk':
            return self.update_walk(dt)
    
    def update_walk(self, dt):
        dt *= .001
        
        vx = self.walking_vector[0]
        vy = self.walking_vector[1]
        
        destx = self.walking_destination[0]
        desty = self.walking_destination[1]
        
        bx = self.walking_direction_boolean[0]
        by = self.walking_direction_boolean[1]
        
        movex = vx * dt
        movey = vy * dt
        
        self.decimal_rect[0] += movex
        self.decimal_rect[1] += movey
        
        if bx:
            int_decimal_rect_x = int(self.decimal_rect[0])
        else:
            int_decimal_rect_x = ceil(self.decimal_rect[0])
        
        if by:
            int_decimal_rect_y = int(self.decimal_rect[1])
        else:
            int_decimal_rect_y = ceil(self.decimal_rect[1])
        
        self.decimal_rect[0] -= int_decimal_rect_x
        self.decimal_rect[1] -= int_decimal_rect_y
        
        self.rect.move_ip(int_decimal_rect_x,
                          int_decimal_rect_y)
        
        rectx = self.rect[0]
        recty = self.rect[1]
        
        recalculate = False
        
        if bx:
            if rectx > destx:
                self.rect.left = destx
                recalculate = True
        else:
            if rectx < destx:
                self.rect.left = destx
                recalculate = True
        
        if by:
            if recty > desty:
                self.rect.top = desty
                recalculate = True
        else:
            if recty < desty:
                self.rect.top = desty
                recalculate = True
        
        if self.rect.left == destx and self.rect.top == desty:
            self.change_act('stand')
        elif recalculate:
            self.set_walk()
        
        return (int_decimal_rect_x, int_decimal_rect_y)

