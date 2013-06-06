import os
import pygame
from pygame import *

import actor_images
import terrain_images
import common
import constants
import terraform

import interface

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
        self.chunk_offset = (0, 0)
        self.tile_offset = (0, 0)
        self.tile_offset_end = (0, 0)
        self.centered_actor_offset = (0, 0) #tuple of actor landscape coordinates
        
        #image caches
        self.actor_images = actor_images.actor_images()
        self.terrain_images = terrain_images.terrain_images()
        
        #render groups
        self.actor_sprite_group = pygame.sprite.Group()
        self.effect_sprite_group = pygame.sprite.Group()
        self.gui_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.RenderUpdates()
        
        self.interface = interface.interface()
        
        for button in self.interface.all_buttons:
            button_element = self.interface.all_buttons[button]
            self.gui_group.add(button_element)
    
    ##########
    # actors #
    ##########
    
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
        
        #place actor at its previous position if it was walking
        if actor.current_act == 'walk':
            if actor == self.centered_actor:
                distance_to_destination =\
                    (actor.walking_destination[0] - actor.rect.left,
                     actor.walking_destination[1] - actor.rect.top)
                #print distance_to_destination
                #shift universe by distance
                self.shift_universe(distance_to_destination)
            
            self.place_actors(place_me=actor, at_walking_destination=True)
        
        old_position = actor.old_position
        
        if new_position == old_position:
            #skipping ahead to pause
            pass
        else:
            new_screen_coordinates = self.screen_coordinates_from_map_position(new_position)
            actor.set_walk(new_screen_coordinates)
            actor.change_act('walk')
    
    def add_ability(self, number_slot, ability_object):
        string_number = str(number_slot)
        element = self.interface.all_buttons[string_number]
        element.load_image(ability_object.image_name)
    
    def remove_ability(self, number_slot):
        string_number = str(number_slot)
        element = self.interface.all_buttons[string_number]
        element.erase_image()
    
    ###############
    # drawing map #
    ###############
    
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
            
            #blit_coords = (tile_offset_x + stagger_offset + self.centered_actor_offset[0],
            #               tile_offset_y + self.centered_actor_offset[1])
            blit_coords = (tile_offset_x + stagger_offset + self.chunk_offset[0] + self.tile_offset[0],
                           tile_offset_y + self.chunk_offset[1] + self.tile_offset[1])
            
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
        stagger_offset = 0
        if upon_actor.position[1] & 1 != 0:
            stagger_offset = self.tile_odd_offset
        
        #move actor's image rect to center
        old_rect = self.centered_actor.rect
        self.centered_actor.rect.left = half_screen_x - half_tile_x
        self.centered_actor.rect.top = half_screen_y - half_tile_y
        
        #calculate terrain offset given actor's position
        centered_actor_offset = (half_screen_x - half_tile_x - tile_offset_x - stagger_offset,
                                 half_screen_y - half_tile_y - tile_offset_y)
        
        #if actor_position[1] & 2 == 1:
        #    centered_actor_offset = (centered_actor_offset[0], centered_actor_offset[1] - half_tile_draw_x)
        
        #import code; code.interact(local=locals())
        
        self.centered_actor_offset = centered_actor_offset
        
        #smaller tile offset
        chunk_size = terraform.chunk_size
        into_tile = (abs(actor_position[0] - (actor_position[0] / chunk_size) * chunk_size),
                     abs(actor_position[1] - (actor_position[1] / chunk_size) * chunk_size))
        
        subtract_tile_offset = (centered_actor_offset[0] - (into_tile[0] * tile_draw_dimensions[0]) - stagger_offset,
                                centered_actor_offset[1] - (into_tile[1] * tile_draw_dimensions[1]))
        
        self.tile_offset = (centered_actor_offset[0] - subtract_tile_offset[0],
                            centered_actor_offset[1] - subtract_tile_offset[1])
        
        #chunk offset
        self.chunk_offset = (centered_actor_offset[0] - self.tile_offset[0],
                             centered_actor_offset[1] - self.tile_offset[1])
    
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
        
        screen_coords = (tile_offset_x + self.tile_offset[0] + stagger_offset + self.centered_actor_offset[0],
                         tile_offset_y + self.tile_offset[1] + self.centered_actor_offset[1])
        
        return screen_coords
    
    def place_actors(self, place_me=None, at_walking_destination=False):
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
            if at_walking_destination:
                #screen_coordinates = self.screen_coordinates_from_map_position(each_actor.old_position)
                screen_coordinates = each_actor.walking_destination
            else:
                screen_coordinates = self.screen_coordinates_from_map_position(each_actor.position)
            
            each_actor.rect.left = screen_coordinates[0]
            each_actor.rect.top = screen_coordinates[1]
    
    def screen_offset_from_map_direction(self, old_map_bounds, new_map_bounds):
        map_change_direction = (old_map_bounds[0][0] - new_map_bounds[0][0],
                                old_map_bounds[1][0] - new_map_bounds[1][0])
        screen_change_direction = (map_change_direction[0] * self.tile_draw_dimensions[0],
                                   map_change_direction[1] * self.tile_draw_dimensions[1])
        return screen_change_direction
    
    def displace_actor(self, displace_me, screen_change_direction):
        #move actor's rect, and its destinations
        displace_me.rect.left += screen_change_direction[0]
        displace_me.rect.top += screen_change_direction[1]
        
        old_walking_destination = displace_me.walking_destination
        displace_me.walking_destination = (old_walking_destination[0] + screen_change_direction[0],
                                           old_walking_destination[1] + screen_change_direction[1])
    
    def shift_tile_offset(self, shift_distance):
        self.tile_offset = (self.tile_offset[0] - shift_distance[0],
                            self.tile_offset[1] - shift_distance[1])
    
    def shift_universe(self, shift_distance):
        #if the centered actor has or will have moved, shift the universe
        self.shift_tile_offset(shift_distance)
        
        #move all other actors' current destination/position
        for each_actor in self.model.actors:
            each_actor.walking_destination = (each_actor.walking_destination[0] - shift_distance[0],
                                              each_actor.walking_destination[1] - shift_distance[1])
            each_actor.rect.left = each_actor.rect.left - shift_distance[0]
            each_actor.rect.top = each_actor.rect.top - shift_distance[1]
        
        ##move center actor itself
        #self.centered_actor.rect.left -= shift_distance[0]
        #self.centered_actor.rect.top  -= shift_distance[1]
    
    ############
    # draw all #
    ############
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_map()
        self.screen.blit(self.terrain, (0, 0))
        
        self.actor_sprite_group.draw(self.screen)
        self.effect_sprite_group.draw(self.screen)
        self.gui_group.draw(self.screen)
        self.text_group.draw(self.screen)
    
    ##########
    # update #
    ##########
    
    def update(self, dt):
        #update animations
        center_walked = None
        for each_actor in self.model.actors:
            if each_actor == self.centered_actor:
                center_walked = each_actor.update_chain(dt)
            else:
                each_actor.update_chain(dt)
        
        if center_walked != None:
            self.shift_universe(center_walked)
        
        #draw sprites as they are now
        self.draw()
        
        self.display.flip()

