#!/usr/bin/env python

from pygame import *

class controller(object):
    def __init__(self, model, event_object):
        self.model = model
        # self.view = model.view
        self.event_object = event_object
        
        self.key_map = {}
        
        direction_key_map = {}
        direction_key_map[K_e] = 1
        direction_key_map[K_d] = 3
        direction_key_map[K_x] = 5
        direction_key_map[K_z] = 7
        direction_key_map[K_a] = 9
        direction_key_map[K_w] = 11
        self.direction_key_map = direction_key_map
    
    def control(self):
        for event in self.event_object.get():
            if event.type == KEYDOWN:
                #test make player and add actor
                if event.key == K_1:
                    self.model.add_player('Aaron', 'human')
                    self.model.add_actor('Doggy', 'dog', 'Aaron', 'human', (0, 0))
                    self.model.actors[-1].speed = 6
                    #self.model.add_actor('Doggy3', 'dog', 'Aaron', 'human', 0, 1)
                    #self.model.actors[-1].speed = 3
                elif event.key == K_2:
                    self.model.add_player('Bill Gates', 'computer')
                    self.model.add_actor('Doggy2', 'dog', 'Bill Gates', 'computer', (6, 2))
                    self.model.actors[-1].speed = 4
                elif event.key == K_3:
                    self.model.initialize_map()
                
                elif event.key == K_m:
                    print self.model.landscape
                elif event.key == K_n:
                    self.model.print_actor()
                
                elif event.key == K_i:
                    self.model.create_item('Leather Gloves', (4, 0))
                elif event.key == K_o:
                    self.model.pick_up_item()
                elif event.key == K_p:
                    if len(self.model.current_actor.inventory) > 0:
                        equip_me = self.model.current_actor.inventory[0]
                        self.model.current_actor.equip_item(equip_me)
                        self.model.current_actor.remove_item(equip_me)
                elif event.key == K_l:
                    unequip_me = self.model.current_actor.unequip_item_at_location('hands')
                    if unequip_me != None:
                        self.model.current_actor.add_item(unequip_me)
                
                elif event.key == K_m:
                    self.model.traverse_portal()
                
                #move actor
                elif event.key in self.direction_key_map:
                    if self.model.current_actor != None:
                        self.model.move_actor(self.direction_key_map[event.key])
                
                #quit
                elif event.key == K_q:
                    return 'main_menu'
