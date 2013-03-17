import os
import pygame
from pygame import *

import actor_images
import terrain_images
import common
import constants

#display is imported from pygame/*

class view(object):
    def __init__(self, screen, display):
        self.screen = screen
        self.background = pygame.Surface((800, 600))
        self.background.fill(constants.background_color)
        self.terrain = pygame.Surface((800, 600))
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.tile_draw_dimensions = (45, 33)
        self.tile_odd_offset = 22.5
        
        self.model = None #intialized manually
        self.display = display
        
        self.centered_actor = None
        self.centered_actor_offset = (0, 0) #tuple of actor landscape coordinates
        
        #image caches
        self.actor_images = actor_images.actor_images()
        self.terrain_images = terrain_images.terrain_images()
        
        #render groups
        self.actor_sprite_group = pygame.sprite.Group()
        self.effect_sprite_group = pygame.sprite.Group()
        self.gui_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.RenderUpdates()
    
    def add_actor(self, new_actor):
        self.actor_images.load_images(new_actor.actor_type)
        
        new_actor.initialize_sprite(self.actor_sprite_group)
        
        new_actor.initialize_animation(self.actor_images.images[new_actor.actor_type])
        new_actor.update_chain(0)
        
        new_actor.rect = new_actor.image.get_rect()
        
        self.actor_sprite_group.add(new_actor)
    
    def move_actor_image(self, actor, newx, newy):
        #the specified actor's image has moved
        #make it walk
        
        if actor.current_act == 'walk':
            #set it to current destination
            actor.rect.left = actor.walking_destination[0]
            actor.rect.top = actor.walking_destination[1]
        
        actor.set_walk(newx, newy)
        
        actor.change_act('walk')
    
    def draw_map(self):
        landscape_min_x = self.model.landscape.landscape_size[0][0]
        landscape_min_y = self.model.landscape.landscape_size[1][0]
        
        self.terrain.fill(constants.background_color)
        for map_coord in self.model.landscape.landscape:
            terrain_type = self.model.landscape.landscape[map_coord].terrain_image_name
            self.terrain_images.load_images(terrain_type)
            
            tile_draw_dimensions = self.tile_draw_dimensions
            
            if map_coord[1] & 1 == 0:
                stagger_offset = 0
            else:
                stagger_offset = self.tile_odd_offset
            
            tile_offset_x = (map_coord[0] - landscape_min_x) * tile_draw_dimensions[0]
            tile_offset_y = (map_coord[1] - landscape_min_y) * tile_draw_dimensions[1]
            
            blit_coords = (tile_offset_x + stagger_offset,
                           tile_offset_y)
            
            self.terrain.blit(self.terrain_images.images[terrain_type],
                              blit_coords)
    
    def center_map(self, upon_actor):
        self.centered_actor = upon_actor
        
        #calculate useful coordinates and measurements
        actor_position = upon_actor.position
        landscape_bounds = self.landscape.landscape_size
        tile_draw_dimensions = self.tile_draw_dimensions
        
        actor_distance_to_edge = (abs(landscape_bounds[0][0] - actor_position[0]),
                                  abs(landscape_bounds[1][0] - actor_position[1]))
        
        half_screen_x = self.terrain.get_width() / 2.0
        half_screen_y = self.terrain.get_height() / 2.0
        
        half_tile_x = tile_draw_dimensions[0] / 2.0
        half_tile_y = tile_draw_dimensions[1] / 2.0
        
        tile_offset_x = actor_distance_to_edge[0] * tile_draw_dimensions[0]
        tile_offset_y = actor_distance_to_edge[1] * tile_draw_dimensions[1]
        
        #odd y stagger offset
        if upon_actor.position[1] & 1 == 0:
            stagger_offset = 0
        else:
            stagger_offset = self.tile_odd_offset
        
        #move actor's image rect to center
        self.centered_actor.rect = ((half_screen_x - half_tile_x,
                                     half_screen_y - half_tile_y))
        
        #calculate terrain offset given actor's position
        centered_actor_offset = (half_screen_x - half_tile_x - tile_offset_x - stagger_offset,
                                 half_screen_y - half_tile_y - tile_offset_y)
        
        if actor_position[1] & 2 == 1:
            centered_actor_offset = (centered_actor_offset[0], centered_actor_offset[1] - half_tile_draw_x)
        print landscape_bounds, actor_position
        print centered_actor_offset
        self.centered_actor_offset = centered_actor_offset
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.terrain, self.centered_actor_offset)
        
        self.actor_sprite_group.draw(self.screen)
        self.effect_sprite_group.draw(self.screen)
        self.gui_group.draw(self.screen)
        self.text_group.draw(self.screen)
  
    def update(self):
        self.draw()
        self.display.flip()

