from dataclasses import dataclass
import random

#TODO:
# whole module:
# move consts to own file

# generate_level():
# add the ability to exclude elements or fills
# add ability to take additional arguments to determine # of colors

# dataclasses and _apply_*()
# add ability to use letters as color variables in elements and fills
# make sure the function checks if there is space on the field
# >>>make function apply leading zeroes

# _weighted_roll()
# fix weighted roll quick fix
# change weighted roll to return element again instead of index

# README.md
# add description to README
# add functions to README
# add string caveat to README -> can only do 0-9 as string
# change references to 9x8 field to 8x8
# add caveat that if you use treat_as_fill on design element you need to deliver one single list
# if not, deliver a list for each row
# change dataclass types for output from int to list

# Fills and Elements
# add all elements and fills from level gen doc

@dataclass
class DesignElement:
    """Level Design Element that provides a string that can be loaded onto the list of bubbles.
    If treat_as_fill is True, make sure to provide an output that will run from the first bubble.
    If not, provide the output in a 2D list with a list per row. Remember to use leading zeroes in your designs when needed."""
    name: str
    cost: int
    chance_weight: int
    output: list
    treat_as_fill: bool = False
    override: bool = True

@dataclass
class Fill:
    """Level Design Fill that can be used to fill in the spaces between design elements."""
    name: str
    cost: int
    chance_weight: int
    output: list
    override: bool = False

@dataclass
class GeneratorConfig:
    """Configuration data for the level generator."""
    base_difficulty: int = 10
    diff_per_level: int = 1
    diff_per_star: int = 1
    field_width: int = 8
    field_height: int = 8

DESIGNS = [ # These are based on default field width and height
    DesignElement(name = 'torii', cost = 6, chance_weight = 1, treat_as_fill = True,
                  output = [2, 0, 0, 0, 0, 0, 0, 2, 
                             2, 2, 2, 2, 2, 2, 2, 
                            0, 0, 2, 0, 0, 2, 0, 0, 
                             0, 2, 2, 2, 2, 2, 0, 
                            0, 2, 0, 0, 0, 0 ,2, 0, 
                             2, 0, 0, 0, 0, 0, 2]),
    DesignElement(name = 'fireworks', cost = 3, chance_weight= 1, override = True,
                  output = [[0, 24, 24, 0],
                             [24, 97, 24]]),    
]

FILLS = [   # These are based on default field width and height
    Fill(name = 'ireland', cost = 1, chance_weight = 4,
         output =[9, 9, 7, 7, 7, 7, 3, 3,
                   9, 9, 7, 7, 7, 3, 3,
                  9, 9, 7, 7, 7, 7, 3, 3,
                   9, 9, 7, 7, 7, 3, 3,
                  9, 9, 7, 7, 7, 7, 3, 3,
                   9, 9, 7, 7, 7, 3, 3,
                  9, 9, 7, 7, 7, 7, 3, 3]),
    Fill(name = 'ireland2', cost = 1, chance_weight = 4,
         output =[9, 9, 7, 7, 7, 7, 3, 3,
                   9, 9, 7, 7, 7, 3, 3,
                  9, 9, 7, 7, 7, 7, 3, 3,
                   9, 9, 7, 7, 7, 3, 3,
                  9, 9, 7, 7, 7, 7, 3, 3,
                   9, 9, 7, 7, 7, 3, 3,
                  9, 9, 7, 7, 7, 7, 3, 3]),
]


def _weighted_roll(elements_set):
    """Return a random index from a list with items with weighted chances"""
    
    # Get the total weight and accumulated weights.
    total_weight = 0
    accumulated_weights = []
    for element in elements_set:
        total_weight += element.chance_weight
        accumulated_weights += [total_weight]

    # Roll on the total weight
    roll = random.randint(0, total_weight)

    # Find the element matching the roll result.
    for element in elements_set:
        if roll < accumulated_weights[elements_set.index(element)]:
            return elements_set.index(element)
        
    return -1 #TODO: fix this, this is a quick fix for falling out of the element sets.

def _get_widest(output):
    """Returns the length of the widest row in the output."""
    widest_row = []
    for row in output:
        if len(row) > len(widest_row):
            widest_row = row
    return len(widest_row)

def _get_starting_index(output, config):
    """Picks a random legal starting location on the grid and returns the starting index and if this is on an odd/even row."""
    starting_index = 0
    widest_row_width = _get_widest(output)
    
    # Pick a random starting location on the playing field.
    # Make sure the entire design fits on the field height-wise.
    y_axis = random.randint(0, config.field_height - len(output))

    # Make it so that we don't cut off the element by accident.
    x_start = widest_row_width - len(output[0])

    # Get correct x_axis offset depending on which row we start on.
    if y_axis % 2 == 0: 
        x_axis = random.randint(x_start, config.field_width - widest_row_width)
        is_odd_row = False
    else:
        x_axis = random.randint(x_start, (config.field_width-1) - widest_row_width)
        is_odd_row = True
    
    # Set starting bubble index, starting with the correct row.
    for row_nr in range(0, y_axis):
        if row_nr % 2 == 0:
            starting_index += config.field_width
        else:
            starting_index += config.field_width-1
            
    # Now move to the correct column.
    starting_index += x_axis
    return starting_index, is_odd_row

def _apply_element(element, list, config = GeneratorConfig()):
    """Applies the output of an element to the list of bubbles."""
    list_to_return = list
    index, is_odd_row = _get_starting_index(element.output, config)

    # Apply the design, row by row.
    for row in element.output:
        for bubble in row:

            if element.override == True or list_to_return[index] == 0:
                if bubble != 0:
                    list_to_return[index] = bubble
            index += 1
        
        # Move to the next row.
        if is_odd_row:
            index += (config.field_width - len(row)-1)
            is_odd_row = False
        else:
            index += (config.field_width - len(row))
            is_odd_row = True
        
    return list_to_return

def _apply_fill(fill, list, config = GeneratorConfig()):
    """Applies the output of a fill to the list of bubbles and returns the new list."""
    list_to_return = list

    for index in range(len(fill.output)):
        if fill.override == True or list_to_return[index] == 0:
            if fill.output[index] != 0:
                list_to_return[index] = int(fill.output[index])

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


def generate_level(world, level, stars=0, config=GeneratorConfig(), elements_set=DESIGNS, fill_set=FILLS, return_string=False):
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
        if selected_element.treat_as_fill:
            bubble_list = _apply_fill(selected_element, bubble_list, config)
        else:
            bubble_list = _apply_element(selected_element, bubble_list, config)

    # Apply the fill to our level
    bubble_list = _apply_fill(selected_fill, bubble_list, config)

    if return_string: # Give output as one string.
        return _list_to_string(bubble_list)
    else: # Give output as 2D List.
        return _list_to_2D(bubble_list)

def test():
    output = generate_level(1,1)
    for row in output:
        test_string = " ".join(map(str, row))
        print(test_string.center(20))
    print("Done!")

test()