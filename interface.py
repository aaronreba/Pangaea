import pygame
import os

class interface():
    def __init__(self):
        weapon_switch = element()
        weapon_switch.rect = (25, 555, 45, 45)
        self.weapon_switch = weapon_switch
        
        ability_1 = element()
        ability_1.rect = (75, 555, 45, 45)
        self.ability_1 = ability_1
        
        ability_2 = element()
        ability_2.rect = (125, 555, 45, 45)
        self.ability_2 = ability_2
        
        ability_3 = element()
        ability_3.rect = (175, 555, 45, 45)
        self.ability_3 = ability_3
        
        ability_4 = element()
        ability_4.rect = (225, 555, 45, 45)
        self.ability_4 = ability_4
        
        ability_5 = element()
        ability_5.rect = (275, 555, 45, 45)
        self.ability_5 = ability_5
        
        ability_6 = element()
        ability_6.rect = (325, 555, 45, 45)
        self.ability_6 = ability_6
        
        ability_7 = element()
        ability_7.rect = (375, 555, 45, 45)
        self.ability_7 = ability_7
        
        ability_8 = element()
        ability_8.rect = (425, 555, 45, 45)
        self.ability_8 = ability_8
        
        ability_9 = element()
        ability_9.rect = (475, 555, 45, 45)
        self.ability_9 = ability_9
        
        all_buttons = {}
        all_buttons['`'] = self.weapon_switch
        all_buttons['1'] = self.ability_1
        all_buttons['2'] = self.ability_2
        all_buttons['3'] = self.ability_3
        all_buttons['4'] = self.ability_4
        all_buttons['5'] = self.ability_5
        all_buttons['6'] = self.ability_6
        all_buttons['7'] = self.ability_7
        all_buttons['8'] = self.ability_8
        all_buttons['9'] = self.ability_9
        self.all_buttons = all_buttons
    
class element(pygame.sprite.Sprite):
    def __init__(self):
        #inherited from Sprite, position on screen
        self.rect = None
        
        #inherited from Sprite
        self.image = None
        pygame.sprite.Sprite.__init__(self)
        blank_image_path = os.path.join(
            'images',
            'buttons',
            'skills',
            'blank.png'
        )
        self.image = pygame.image.load(blank_image_path).convert_alpha()
    
    def load_image(self, image_name):
        image_path = os.path.join(
            'images',
            'buttons',
            'skills',
            image_name
        )
        self.image = pygame.image.load(image_path).convert_alpha()
    
    def erase_image(self):
        blank_image_path = os.path.join(
            'images',
            'buttons',
            'skills',
            'blank.png'
        )
        self.image = pygame.image.load(blank_image_path).convert_alpha()

