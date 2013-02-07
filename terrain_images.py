#!/usr/bin/env python

import os
import pygame

class terrain_images(object):
    def __init__(self):
        self.images = {}
    
    def load_images(self, terrain_type):
        if terrain_type in self.images:
            return
        
        self.images[terrain_type] = None
        
        terrain_image = pygame.image.load(os.path.join(
            'images',
            'terrain',
            terrain_type + '.png'
        )).convert_alpha()
        
        self.images[terrain_type] = terrain_image
    
    def remove_images(terrain_type):
        self.images.pop(terrain_type)