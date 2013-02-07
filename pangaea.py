#!/usr/bin/env python

import os
import pygame

# if os.system('python make_install.py build_ext --inplace') == 0:
#     pass
# else:
#     raise SyntaxError

import states

def main():
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((800, 600))
    
    pygame.display.set_caption('Pangaea')
    
    state_manager = states.states(screen)
    state_manager.load_state('main_menu')
    
    while state_manager.run:
        clock.tick(60)
        dt = clock.get_time()
        state_manager.update(dt)
    
    pygame.quit()

if __name__ == '__main__':
    main()
    pygame.quit()
