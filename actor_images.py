import os
import pygame

#the images dict is like so:
#images['dog']['walk'][direction oclock] = [[walk_1_a, walk_2_a, walk_3_a], [walk_1_b, walk_2_b]]
class actor_images(object):
    def __init__(self):
        self.images = {}
    
    def load_images(self, actor_type):
        if actor_type in self.images:
            return
        
        self.images[actor_type] = {}
        
        actor_type_dir = os.path.join('images', 'actors', actor_type)
        
        for action_type in os.listdir(actor_type_dir):
            action_type_dir = os.path.join(actor_type_dir, action_type)
            
            self.images[actor_type][action_type] = {}
            
            for direction in xrange(1, 13, 2):
                self.images[actor_type][action_type][direction] = []
            
            current_frame = None
            current_direction = None
            
            for action_iteration in sorted(os.listdir(action_type_dir)):
                if action_iteration[-4:] != '.png':
                    continue
                
                split_action_iteration = action_iteration.\
                                         split('.')[0].\
                                         split('_')
                direction   = int(split_action_iteration[0])
                chain_index = int(split_action_iteration[1])
                frame_index = int(split_action_iteration[2])
                
                frame_image_name = os.path.join(
                    'images',
                    'actors',
                    actor_type,
                    action_type,
                    action_iteration
                )
                frame = pygame.image.load(frame_image_name).convert_alpha()
                
                
                direction_chain = self.images[actor_type][action_type][direction]
                if len(direction_chain) == chain_index:
                    direction_chain.append([])
                direction_chain[chain_index].append(frame)
    
    def remove_images(actor_type):
        self.images.pop(actor_type)

