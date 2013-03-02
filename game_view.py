import os
import pygame
from pygame import *

import actor_images
import terrain_images
import common

#display is imported from pygame/*

class view(object):
    def __init__(self, screen, display):
        self.screen = screen
        self.background = pygame.Surface((800, 600))
        self.terrain = pygame.Surface((800, 600))
        
        #camera indicates how far the background terrain image should be pushed
        self.camera_x = 0
        self.camera_y = 0
        
        self.model = None #intialized manually
        self.display = display
        
        #image caches
        self.actor_images = actor_images.actor_images()
        self.terrain_images = terrain_images.terrain_images()
        
        #render groups
        self.actor_sprite_group = pygame.sprite.Group()
        self.effect_sprite_group = pygame.sprite.Group()
        self.gui_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.RenderUpdates()
    
    def add_actor(self, new_actor):
        pass
        #self.actor_images.load_images(new_actor.actor_type)
        #
        #new_actor.initialize_sprite(self.actor_sprite_group)
        #
        #new_actor.initialize_animation(self.actor_images.images[new_actor.actor_type])
        #new_actor.update_chain(0)
        #
        #new_actor.display_x = self.camera_x
        #new_actor.display_y = self.camera_y
        #
        #new_actor.rect = new_actor.image.get_rect()
        #self.move_actor_image(new_actor, new_actor.x, new_actor.y)
    
    def move_actor_image(self, actor, newx, newy):
        pass
        ##the specified actor's image has moved
        ##make it walk
        #
        #if actor.current_act == 'walk':
        #    #set it to current destination
        #    actor.rect.left = actor.walking_destination[0]
        #    actor.rect.top = actor.walking_destination[1]
        #
        #actor.set_walk(newx, newy)
        #
        #actor.change_act('walk')
    
    def draw_map(self):
        for map_coord in self.model.landscape.landscape:
            terrain_type = self.model.landscape.landscape[map_coord].terrain_image_name
            self.terrain_images.load_images(terrain_type)
          
            if map_coord[1] & 1 == 0:
                x_offset = 0
            else:
                x_offset = 22.5
          
            blit_coords = (map_coord[0] * 45 + x_offset, map_coord[1] * 33)
            self.terrain.blit(self.terrain_images.images[terrain_type],
                              blit_coords)
  
    def draw(self):
        #redraw tiles that are currently occupied x
        #redraw actors y
        #projectiles x
      
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.terrain, (0, 0))
      
        self.actor_sprite_group.draw(self.screen)
        self.effect_sprite_group.draw(self.screen)
        self.gui_group.draw(self.screen)
        self.text_group.draw(self.screen)
  
    def update(self):
        pass
        self.draw()
        self.display.flip()
