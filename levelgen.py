from dataclasses import dataclass
import random

@dataclass
class DesignElement:
    """Level Design Element that provides a string that can be loaded onto the level arrays."""
    name: str
    cost: int
    chance: int
    output: str
    override: bool = False

@dataclass
class Fill:
    """Level Design Fill that can be used to fill in the spaces between design elements."""
    name: str
    cost: int
    chance: int
    output: str
    override: bool = False

@dataclass
class GeneratorConfig:
    """Configuration data for the level generator."""
    base_difficulty: int = 10
    diff_per_level: int = 1
    diff_per_star: int = 1
    field_width: int = 9
    field_height: int = 8

DESIGN_ELEMENTS = [ # These are based on default field width and height
    DesignElement(name = 'torii', cost = 1, chance = 1, 
                  output ='200000022222222002002000222220020000202000002')
]

FILLS = [   # These are based on default field width and height
    Fill(name = 'ireland', cost = 1, chance = 1, 
         output ='')
]

def _weighted_roll(elements_set):
    """Return a random item with a weighted chance""" #thank you, Lemon ^^
    
    # Get the total chance
    total = sum([element.chance for element in elements_set])

    # Roll some number between 0 and the total of all weighted chances
    roll = random.randint(0, total + 1)

    # Let's find our winner
    chance_so_far = 0    
    for element in elements_set:

        # Offset the chance by chance_so_far, otherwise the roll might 
        # be higher than even the highest item.chance
        if roll < (chance_so_far + element.chance):
            return element
        else:
            chance_so_far += element.chance
            
def _apply_element(element, list, config = GeneratorConfig()):
    list_to_return = []
    return list_to_return

def _apply_fill(fill, list, config = GeneratorConfig()):
    list_to_return = []
    return list_to_return

def _list_to_2D(list):
    return list

def _list_to_string(list):
    return list

def generate_level(world, level, stars, config=GeneratorConfig(), elements_set=DESIGN_ELEMENTS, fill_set=FILLS, return_string=False):
    """Generates a 2d Array or string that contains all of the integers for the level .JSON-file 
    based on entered config parameters, element and fill arrays."""

    # Get total difficulty to spend on this level.
    level_difficulty = (config.base_difficulty * world) + (config.diff_per_level * level) + (config.diff_per_star * stars)
    spent_difficulty = 0

    # Make bubble list, the field has a base width at even height numbers, and width-1 at odd numbers.
    bubble_list = []
    for height in range(0, config.field_height):
        if height % 2 == 0:
            bubble_list += ([0] * config.field_width)
        else:
            bubble_list += ([0] * (config.field_width-1))

    # Pick a random fill, save it for later, and add the cost to what we have spent.
    selected_fill = _weighted_roll(fill_set)
    #spent_difficulty += selected_fill.cost

    # Roll design elements, apply them, and add the cost to what we have spent.
    while spent_difficulty < level_difficulty:
        selected_element = _weighted_roll(elements_set)
        #spent_difficulty += selected_element.cost
        bubble_list = _apply_element(selected_element, bubble_list)
        break

    # Apply the fill to our level
    bubble_list = _apply_fill(selected_fill, bubble_list)

    if return_string: # Give output as one string.
        return _list_to_string(bubble_list)
    else: # Give output as 2D List.
        return _list_to_2D(bubble_list)
    
print(generate_level(1,1,1))