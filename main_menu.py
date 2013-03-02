import os
import pygame
from pygame import *

class view(object):
    def __init__(self, screen, display):
        self.screen = screen
      
        self.background = pygame.Surface((800, 600))
      
        self.background_image = pygame.image.load(os.path.join(
            'images',
            'menus',
            'main_menu.png'
        )).convert_alpha()
      
        self.model = None #intialized manually
        self.display = display
      
        #self.background_sprite_group = pygame.sprite.Group()
        #self.actor_sprite_group = pygame.sprite.Group()
        #self.effect_sprite_group = pygame.sprite.Group()
        #self.text_sprite_group = pygame.sprite.RenderUpdates()
      
        self.draw()
        self.display.flip()
  
    def draw(self):
        #redraw background
        self.background.blit(self.background_image, (0, 0))
        self.screen.blit(self.background, (0, 0))
        pass
  
    def update(self):
        pass

class model(object):
    def __init__(self, view):
        self.view = view
        self.run = True
    
    def update(self, dt):
        pass

class controller(object):
    def __init__(self, model, event_object):
        self.model = model
        self.view = model.view
        self.event_object = event_object
    
    def control(self):
        for event in self.event_object.get():
            if event.type == KEYDOWN:
                if event.key == K_t:
                    #test
                    return 'test_game'
                elif event.key == K_q:
                    #tell model to quit
                    self.run = False
                    return 'quit'
