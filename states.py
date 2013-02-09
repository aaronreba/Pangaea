#!/usr/bin/env python

import pygame
from pygame import *

import main_menu

import game_controller_test
import game_controller
import game_model
import game_view

import terraform

class states(object):
    def __init__(self, screen):
        self.current_state = None
        
        self.run = True
        
        self.screen = screen
    
    def load_state(self, new_state):
        self.current_state = new_state
        self.pass_map = {}
        self.pass_map[None] = None
        
        self.screen.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MAX)
        
        if self.current_state == 'main_menu':
            # self.view = game_view.view(self.screen, display)
            self.model = game_model.model()
            self.controller = main_menu.controller(self.model, pygame.event)
            # self.view.model = self.model
        
        elif self.current_state == 'game':
            # self.view = game_view.view(self.screen, display)
            self.model = game_model.model()
            self.controller = game_controller.controller(self.model, pygame.event)
            # self.view.model = self.model
        
        elif self.current_state == 'test_game':
            # self.view = game_view.view(self.screen, display)
            self.model = game_model.model()
            self.controller = game_controller_test.controller(self.model, pygame.event)
            # self.view.model = self.model
            
            self.model.landscape = terraform.make_terrain_test('basic_grass')
            
            # self.view.draw_map()
    
    def unload_state(self):
        # del self.view
        del self.model
        del self.controller
    
    def update(self, dt):
        self.model.update(dt)
        # self.view.update()
        control_result = self.controller.control()
        
        #control_result is None most of the time.
        #when it is not None, it's a state change.
        try:
            self.pass_map[control_result]
        except:
            if control_result == 'quit':
                self.run = False
            #elif control_result == 'test_game' or\
            #     control_result == 'main_menu':
            else:
                self.unload_state()
                self.load_state(control_result)
