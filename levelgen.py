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
    """Return a random item with a weighted chance"""
    
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
            
def _apply_element(element):
    pass

def _apply_fill(fill):
    pass

def _list_to_array(list):
    pass

def _list_to_string(list):
    pass

def generate_level(config, elements_set, fill_set, return_string=False):
    # get difficulty to spend
    # make bubble list
    # grab max row -> determine how manyth bubble from config
    # pick fill and save it -> deduct cost
    # grab design elements
    # apply fill
    # if return_string:
        # give output as one string
    # if not:
        # give output as 2d array
    pass