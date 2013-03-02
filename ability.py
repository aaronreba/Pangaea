class ability(object):
    def __init__(self, name, weapon_type, level, modifiers):
        self.name = name
        self.weapon_type = weapon_type
        
        #level is the level at which this ability is available
        #according to the weapon level of the character
        self.level = level
        
        #modifiers hold anycombat related information
        self.modifiers = modifiers

#################
# hoovy weapons #
#################
#hoovy strike
heavy_strike_modifiers = {}
heavy_strike_modifiers['range'] = 1
heavy_strike_modifiers['cooldown'] = 0
heavy_strike_modifiers['damage_modifier'] = 1.5
heavy_strike = ability('Heavy Strike', 'heavy_melee', 1, heavy_strike_modifiers)

#leaping strike
leaping_strike_modifiers = {}
leaping_strike_modifiers['range'] = 2
leaping_strike_modifiers['cooldown'] = 0
leaping_strike_modifiers['damage_modifier'] = 2.0
leaping_strike_modifiers['jump'] = 1 #jump is positive, jumping toward
leaping_strike = ability('Leaping Strike', 'heavy_melee', 2, leaping_strike_modifiers)

################
# long weapons #
################
#long strike
long_strike_modifiers = {}
long_strike_modifiers['range'] = 2
long_strike_modifiers['cooldown'] = 0
long_strike_modifiers['damage_modifier'] = 1.25
long_strike_modifiers['strike_through'] = True
long_strike = ability('Long Strike', 'long_melee', 1, long_strike_modifiers)

#retreating strike
retreating_strike_modifiers = {}
retreating_strike_modifiers['range'] = 2
retreating_strike_modifiers['cooldown'] = 0
retreating_strike_modifiers['damage_modifier'] = 1.0
retreating_strike_modifiers['jump'] = -1 #jump is negative, jumping away
retreating_strike = ability('Retreating Strike', 'long_melee', 2, retreating_strike_modifiers)

