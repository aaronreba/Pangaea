from pygame import *

class controller(object):
    def __init__(self, model, event_object):
        self.model = model
        self.view = model.view
        self.event_object = event_object
        
        self.key_map = {}
    
    def control(self):
        for event in self.event_object.get():
            if event.type == KEYDOWN:
                if False:
                    pass
                elif event.key == K_q:
                    return 'main_menu'
