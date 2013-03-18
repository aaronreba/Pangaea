import os
import pygame

terrain_to_image_name = {}
terrain_to_image_name['grass']       = 'light_green_hex'
terrain_to_image_name['heavy_grass'] = 'green_hex'
terrain_to_image_name['jungle']      = 'dark_green_hex'
terrain_to_image_name['forest']      = 'brown_green_hex'
terrain_to_image_name['tundra']      = 'white_hex'
terrain_to_image_name['desert']      = 'orange_hex'
terrain_to_image_name['plains']      = 'yellow_hex'

class terrain_images(object):
    def __init__(self):
        self.images = {}
    
    def load_images(self, terrain_type):
        if terrain_type in self.images:
            return
        
        terrain_image = pygame.image.load(os.path.join(
            'images',
            'terrain',
            terrain_to_image_name[terrain_type] + '.png'
        )).convert_alpha()
        
        self.images[terrain_type] = terrain_image
    
    def remove_images(terrain_type):
        del self.images[terrain_type]
