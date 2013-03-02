class player(object):
    def __init__(self, name, player_type):
        self.name = name
        self.player_type = player_type
        
        #actors owned is a list of indeces of the actors
        #in the model
        self.actors_owned = []
        
