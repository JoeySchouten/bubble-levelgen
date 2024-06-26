from dataclasses import dataclass
import random

@dataclass
class DesignElement:
    """Level Design Element that provides a string that can be loaded onto the level arrays."""
    name: str
    cost: int
    chance_weight: int
    output: str
    override: bool = False

@dataclass
class Fill:
    """Level Design Fill that can be used to fill in the spaces between design elements."""
    name: str
    cost: int
    chance_weight: int
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

DESIGNS = [ # These are based on default field width and height
    DesignElement(name = 'torii', cost = 1, chance_weight = 1,
                  output ='200000022222222002002000222220020000202000002'),
    DesignElement(name = 'torii2', cost = 1, chance_weight = 1, 
                  output ='200000022222222002002000222220020000202000002')            
]

FILLS = [   # These are based on default field width and height
    Fill(name = 'ireland', cost = 1, chance_weight = 4,
         output ='222222'),
    Fill(name = 'ireland2', cost = 1, chance_weight = 4,
         output ='222222')
]


def _weighted_roll(elements_set):
    """Return a random index from a list with items with weighted chances"""
    
    # Get the total weight and accumulated weights
    total_weight = 0
    accumulated_weights = []
    for element in elements_set:
        total_weight += element.chance_weight
        accumulated_weights += [total_weight]

    # Roll some number between 0 and the total of all weighted chances
    roll = random.randint(0, total_weight)

    # Let's find our winner
    for element in elements_set:
        if roll < accumulated_weights[elements_set.index(element)]:
            return elements_set.index(element)
        
    return -1 #TODO: fix this, this is a quick fix for falling out of the element sets.


def _apply_element(element, list, config = GeneratorConfig()):
    """Applies the output of a design element to the list of bubbles and returns the new list."""
    list_to_return = list

    for bubble in element.output:
        if element.override == True:
            list_to_return += [bubble]
        elif list[element.output.index(bubble)] == 0:
            list_to_return += [bubble]
        else:
            list_to_return += [list[element.output.index(bubble)]]

    return list_to_return


def _list_to_2D(list, config = GeneratorConfig()):
    """Changes the bubble list input to a 2D List to return."""
    list_to_return = []
    for index in range(0, config.field_height):
        temp_list = []
        if index % 2 == 0:
            for i in range(0, config.field_width):
                temp_list.append(list.pop(0))
        else:
            for i in range(0, config.field_width-1):
                temp_list.append(list.pop(0))
        list_to_return.append(temp_list)
    return list_to_return


def _list_to_string(list):
    """Changes the bubble list input to a string to return."""
    string_to_return = ''

    for entry in list:
        string_to_return += str(entry)
    
    return string_to_return


def generate_level(world, level, stars, config=GeneratorConfig(), elements_set=DESIGNS, fill_set=FILLS, return_string=False):
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
    selected_fill = fill_set[_weighted_roll(fill_set)]
    spent_difficulty += selected_fill.cost

    # Roll design elements, apply them, and add the cost to what we have spent.
    while spent_difficulty < level_difficulty:
        selected_element = elements_set[_weighted_roll(elements_set)]
        spent_difficulty += selected_element.cost
        bubble_list = _apply_element(selected_element, bubble_list)
        break

    # Apply the fill to our level
    bubble_list = _apply_element(selected_fill, bubble_list)

    if return_string: # Give output as one string.
        return _list_to_string(bubble_list)
    else: # Give output as 2D List.
        return _list_to_2D(bubble_list)
    
print(generate_level(1,1,1))