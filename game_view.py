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
    
    def remove_actor(self, remove_me):
        self.actor_sprite_group.remove(remove_me)
    
    def move_actor_image(self, actor):
        #assumes map coordinates
        #the specified actor's image has moved
        #make it walk
        
        new_position = actor.position
        
        screen_coordinates = self.screen_coordinates_from_map_position(new_position)
        
        #place actor at its previous position
        self.place_actors(place_me=actor, at_old=True)
        
        actor.set_walk(screen_coordinates)
        
        actor.change_act('walk')
    
    def draw_map(self):
        if self.model.landscape == None:
            return
        landscape_min_x = self.model.landscape.landscape_size[0][0]
        landscape_min_y = self.model.landscape.landscape_size[1][0]
        
        self.terrain.fill(constants.background_color)
        for map_coord in self.model.landscape.landscape:
            terrain_type = self.model.landscape.landscape[map_coord].terrain_type
            self.terrain_images.load_images(terrain_type)
            
            tile_draw_dimensions = self.tile_draw_dimensions
            
            if map_coord[1] & 1 == 0:
                stagger_offset = 0
            else:
                stagger_offset = self.tile_odd_offset
            
            tile_offset_x = (map_coord[0] - landscape_min_x) * tile_draw_dimensions[0]
            tile_offset_y = (map_coord[1] - landscape_min_y) * tile_draw_dimensions[1]
            
            blit_coords = (tile_offset_x + stagger_offset + self.centered_actor_offset[0],
                           tile_offset_y + self.centered_actor_offset[1])
            
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
        old_rect = self.centered_actor.rect
        self.centered_actor.rect.left = half_screen_x - half_tile_x
        self.centered_actor.rect.top = half_screen_y - half_tile_y
        
        #calculate terrain offset given actor's position
        centered_actor_offset = (half_screen_x - half_tile_x - tile_offset_x - stagger_offset,
                                 half_screen_y - half_tile_y - tile_offset_y)
        
        if actor_position[1] & 2 == 1:
            centered_actor_offset = (centered_actor_offset[0], centered_actor_offset[1] - half_tile_draw_x)
        #import code; code.interact(local=locals())
        self.centered_actor_offset = centered_actor_offset
    
    def screen_coordinates_from_map_position(self, map_position):
        landscape_min_x = self.model.landscape.landscape_size[0][0]
        landscape_min_y = self.model.landscape.landscape_size[1][0]
        
        self.terrain.fill(constants.background_color)
        
        tile_draw_dimensions = self.tile_draw_dimensions
        
        if map_position[1] & 1 == 0:
            stagger_offset = 0
        else:
            stagger_offset = self.tile_odd_offset
        
        tile_offset_x = (map_position[0] - landscape_min_x) * tile_draw_dimensions[0]
        tile_offset_y = (map_position[1] - landscape_min_y) * tile_draw_dimensions[1]
        
        blit_coords = (tile_offset_x + stagger_offset + self.centered_actor_offset[0],
                       tile_offset_y + self.centered_actor_offset[1])
        
        return blit_coords
    
    def place_actors(self, place_me=None, at_old=False):
        #centered_actor = self.centered_actor
        #
        #if place_me == None:
        #    draw_me = self.model.actors
        #else:
        #    draw_me = [place_me]
        #
        #for each_actor in draw_me:
        #    screen_coordinates = self.screen_coordinates_from_map_position(each_actor.position)
        #    
        #    old_rect = each_actor.rect
        #    each_actor.rect.left = screen_coordinates[0]
        #    each_actor.rect.top = screen_coordinates[1]
        
        if place_me == None:
            draw_me = self.model.actors
        else:
            draw_me = [place_me]
        
        for each_actor in draw_me:
            if at_old:
                screen_coordinates = self.screen_coordinates_from_map_position(each_actor.old_position)
            else:
                screen_coordinates = self.screen_coordinates_from_map_position(each_actor.position)
            
            each_actor.rect.left = screen_coordinates[0]
            each_actor.rect.top = screen_coordinates[1]
    
    def screen_offset_from_map_direction(self, old_map_bounds, new_map_bounds):
        map_change_direction = (old_map_bounds[0][0] - new_map_bounds[0][0],
                                old_map_bounds[1][0] - new_map_bounds[1][0])
        if map_change_direction[1] & 1 == 1:
            x_offset = self.tile_draw_dimensions[0] / 2.0
            if new_map_bounds[1][0] & 1 == 1:
                #even to odd: add half of x width
                pass
            else:
                #odd to even: subtract half
                x_offset = -x_offset
        else:
            x_offset = 0
        screen_change_direction = (map_change_direction[0] * self.tile_draw_dimensions[0] + x_offset,
                                   map_change_direction[1] * self.tile_draw_dimensions[1])
        return screen_change_direction
    
    def displace_actor(self, displace_me, screen_change_direction):
        #move actor's rect, and its destinations
        displace_me.rect.left += screen_change_direction[0]
        displace_me.rect.top += screen_change_direction[1]
        
        old_walking_destination = displace_me.walking_destination
        displace_me.walking_destination = (old_walking_destination[0] + screen_change_direction[0],
                                           old_walking_destination[1] + screen_change_direction[1])
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_map()
        self.screen.blit(self.terrain, (0, 0))
        
        self.actor_sprite_group.draw(self.screen)
        self.effect_sprite_group.draw(self.screen)
        self.gui_group.draw(self.screen)
        self.text_group.draw(self.screen)
    
    def update(self, dt):
        #update animations
        for each_actor in self.model.actors:
            each_actor.update_chain(dt)
        
        #draw sprites as they are now
        self.draw()
        
        self.display.flip()

