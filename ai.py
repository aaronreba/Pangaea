class ai(object):
    def __init__(self):
        self.mood = 'normal'
        self.behavior = 'runner'
        
        #if the ai is closer than this value, run.
        #1 = melee
        #maybe a ranged character is a 4. its spells are range 4.
        #if that character is at exactly range 4, it will attack.
        #else run.
        self.behavior_running_distance = (3, 4)
        
        #target is an actor
        self.target = None
    
    def is_distance_in_running(self, a_distance):
        if self.behavior_running_distance[0] <= a_distance <= self.behavior_running_distance[1]:
            return 0
        elif a_distance < self.behavior_running_distance[0]:
            return -1
        else:
            return 1
    
    #i'm using setters and accessors so i don't make a typo typing "normal"
    
    def set_behavior_runner(self):
        self.behavior = 'runner'
    def set_behavior_chaser(self):
        self.behavior = 'chaser'
    
    def is_behavior_runner(self):
        return self.behavior == 'runner'
    def is_behavior_chaser(self):
        return self.behavior == 'chaser'
    
    def set_mood_normal(self):
        self.mood = 'normal'
    def set_mood_afraid(self):
        self.mood = 'afraid'
    def set_mood_berserk(self):
        self.mood = 'berserk'
    def set_mood_resting(self):
        self.mood = 'resting'
    
    def is_mood_normal(self):
        return self.mood == 'normal'
    def is_mood_afraid(self):
        return self.mood == 'afraid'
    def is_mood_berserk(self):
        return self.mood == 'berserk'
    def is_mood_resting(self):
        return self.mood == 'resting'

