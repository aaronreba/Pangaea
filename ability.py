class ability(object):
    def __init__(self, name, image_name, modifiers):
        self.name = name
        self.image_name = image_name
        
        #modifiers hold anycombat related information
        self.modifiers = modifiers

#################
# hoovy weapons #
#################
#hoovy strike
heavy_strike_modifiers = {}
heavy_strike_modifiers['level'] = 1
heavy_strike_modifiers['weapon_type'] = 'heavy_melee'
heavy_strike_modifiers['range'] = 1
heavy_strike_modifiers['cooldown'] = 0
heavy_strike_modifiers['damage_modifier'] = 1.5
heavy_strike = ability('Heavy Strike', 'template.png', heavy_strike_modifiers)

#leaping strike
leaping_strike_modifiers = {}
leaping_strike_modifiers['level'] = 1
leaping_strike_modifiers['weapon_type'] = 'heavy_melee'
leaping_strike_modifiers['range'] = 2
leaping_strike_modifiers['cooldown'] = 0
leaping_strike_modifiers['damage_modifier'] = 2.0
leaping_strike_modifiers['jump'] = 1 #jump is positive, jumping toward
leaping_strike = ability('Leaping Strike', 'template.png', leaping_strike_modifiers)

################
# long weapons #
################
#long strike
long_strike_modifiers = {}
long_strike_modifiers['level'] = 1
long_strike_modifiers['weapon_type'] = 'heavy_melee'
long_strike_modifiers['range'] = 2
long_strike_modifiers['cooldown'] = 0
long_strike_modifiers['damage_modifier'] = 1.25
long_strike_modifiers['strike_through'] = True
long_strike = ability('Long Strike', 'template.png', long_strike_modifiers)

#retreating strike
retreating_strike_modifiers = {}
retreating_strike_modifiers['level'] = 1
retreating_strike_modifiers['weapon_type'] = 'heavy_melee'
retreating_strike_modifiers['range'] = 2
retreating_strike_modifiers['cooldown'] = 0
retreating_strike_modifiers['damage_modifier'] = 1.0
retreating_strike_modifiers['jump'] = -1 #jump is negative, jumping away
retreating_strike = ability('Retreating Strike', 'template.png', retreating_strike_modifiers)

