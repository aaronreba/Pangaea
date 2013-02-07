import random

#% chance that a random terrain hex will have an item:
random_terrain_chance = 100

class NoItemFound(Exception):
    def __init__(self, item_name):
        self.item_name = item_name
    def __str__(self):
        return 'Item not found: ' + self.item_name

class item(object):
    def __init__(self, item_name):
        self.get_item(item_name)
    
    def __str__(self):
        print_me = ''
        print_me +=\
'''
Name: {0}
Type: {1}
Description: {2}
Location: {3}
Level: {4}
Stats: {5}
'''.format(self.name, self.type, self.description, self.location, self.level, str(self.stats))
        return print_me
    
    
    def get_item(self, item_name):
        item_file = open('item_list.txt', 'r')
        for line in item_file:
            if line.split(',')[0] == item_name:
                break
        else:
            raise NoItemFound(item_name)
        
        item_file.close()
        
        line = line.rstrip()
        
        line = line.split(',')
        
        self.name = line[0].strip()
        self.type = line[1].strip()
        self.image = line[2].strip()
        self.description = line[3].strip()
        self.location = line[4].strip()
        self.level = line[5].strip()
        self.stats = {}
        for stat_modifier in line[6:]:
            stat_modifier = stat_modifier.strip()
            stat = stat_modifier.split(':')[0]
            modifier = int(stat_modifier.split(':')[1])
            self.stats[stat] = modifier

def generate_random_with_chance(level=None):
    if random.randint(0, 99) < random_terrain_chance:
        return generate_random(level)

def generate_random(level=None):
    #if level is none, generate absolutely random item
    #else, generate item with level in that range inclusively
    while 1:
        item_file = open('item_list.txt', 'r')
        
        for j, line in enumerate(item_file):
            pass
        
        good_index = True
        
        random_index = random.randint(0, j - 1)
        
        while good_index:
            item_file.seek(0)
            for i, line in enumerate(item_file):
                if i == random_index:
                    if line == '\n' or line[0] == '#':
                        good_index = False
                    break
            
            if not good_index:
                #reroll index
                random_index = random.randint(0, j - 1)
            else:
                if level == None:
                    break
                else:
                    resolved_item = item(line.split(',')[0])
                    if level[0] <= int(resolved_item.level) <= level[1]:
                        break
                    else:
                        pass
            
            good_index = True
        
        item_file.close()
        
        return resolved_item
