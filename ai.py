class ai(object):
    def __init__(self):
        self.mood = 'normal'
        
        #if the ai is closer than this value, run.
        #1 = melee
        #maybe a ranged character is a 4. its spells are range 4.
        #if that character is at exactly range 4, it will attack.
        #else run.
        self.behavior_running_distance = 1
        
        #target is an actor
        self.target = None
    
    #i'm using setters and accessors so i don't make a typo typing "normal"
    
    def set_mood_normal(self):
        self.mood = 'normal'
    def set_mood_afraid(self):
        self.mood = 'afraid'
    def set_mood_berserk(self):
        self.mood = 'berserk'
    def set_mood_chase(self):
        self.mood = 'chase'
    def set_mood_resting(self):
        self.mood = 'resting'
    
    def is_mood_normal(self):
        return self.mood == 'normal'
    def is_mood_afraid(self):
        return self.mood == 'afraid'
    def is_mood_berserk(self):
        return self.mood == 'berserk'
    def is_mood_chase(self):
        return self.mood == 'chase'
    def is_mood_resting(self):
        return self.mood == 'resting'
