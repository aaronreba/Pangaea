#!/usr/bin/env python

import os
import pygame

#the images dict is like so:
#images['actor_type'] = {'act': [frame_1, ...]...}
#for example:
#images['dog']['walk'] = [walk_1, walk_2, walk_3]
class actor_images(object):
    def __init__(self):
        self.images = {}
    
    def load_images(self, actor_type):
        if actor_type in self.images:
            return
        
        self.images[actor_type] = {}
        
        actor_image_data = open('actor_image_data.txt', 'r')
        
        while actor_image_data.readline()[2:-1] != actor_type:
            pass
        
        frame_chain = []
        
        while 1:
            line = actor_image_data.readline()
            if not line or line[0] == '>' or line == '\n':
                break
            
            short_line = line[2:-1]
            if line[0] == '#':
                #new act
                if frame_chain:
                    self.images[actor_type][act].append(frame_chain)
                
                act = short_line
                self.images[actor_type][act] = []
                chain_number = 0
                frame_chain = []
            elif line[0] == ':':
                #new frame
                frame = pygame.image.load(os.path.join(
                    'images',
                    'actors',
                    actor_type,
                    act,
                    short_line
                )).convert_alpha()
                if short_line[0] == str(chain_number):
                    frame_chain.append(frame)
                else:
                    self.images[actor_type][act].append(frame_chain)
                    frame_chain = []
                    chain_number += 1
                frame_chain.append(frame)
                
        
        self.images[actor_type][act].append(frame_chain)
        
        actor_image_data.close()
    
    def remove_images(actor_type):
        self.images.pop(actor_type)