from dataclasses import dataclass

from consts import DESIGNS, FILLS

from helpers import _apply_element, _apply_fill, _filter_list, _list_to_2D, _list_to_string, _weighted_roll

#TODO:
# generate_level():
# add ability to take additional arguments to determine # of colors

# dataclasses and _apply_*()
# add ability to use letters as color variables in elements and fills       PRIO_2
# add ability to set colors for these -> if none just random
# add min/max start row position                                            PRIO_3

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

# Balancing
# Adjust numbers on everything

@dataclass
class GeneratorConfig:
    """Configuration data for the level generator."""
    base_difficulty: int = 10
    diff_per_level: int = 1
    diff_per_star: int = 1
    field_width: int = 8
    field_height: int = 8


def generate_level(world, level, stars=0, config=GeneratorConfig(), required=[], excludes=[], elements_set=DESIGNS, fill_set=FILLS, return_string=False, only_required=False):
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

    # Select a fill either based on a pre-defined name or from the constant, filtered or not.
    fills_to_roll = []
    selected_fill = None

    # See if we have a fill defined; We can only use one fill, so we stop as soon as we find one pre-defined.
    for fill in fill_set:
        if fill.name in required:
            selected_fill = fill
            break
    
    # If we have no pre-defined fills, filter the list of fills using the excluding keywords, and roll on the result.
    if selected_fill is None:
        fills_to_roll = _filter_list(excludes, fill_set)
        selected_fill = fills_to_roll[_weighted_roll(fills_to_roll)]
    spent_difficulty += selected_fill.cost

    # Take the required names and queue all elements that are predefined, then apply them.
    queued_elements = []
    for element in elements_set:
        if element.name in required:
            queued_elements.append(element)
    
    for element in queued_elements:
        spent_difficulty += element.cost
        if element.treat_as_fill:
            bubble_list = _apply_fill(element, bubble_list, config)
        else:
            bubble_list = _apply_element(element, bubble_list, config)

    # Roll design elements, apply them, and add the cost to what we have spent.
    elements_to_roll = _filter_list(excludes, elements_set)
    while spent_difficulty < level_difficulty and not only_required:
        selected_element = elements_to_roll[_weighted_roll(elements_to_roll)]
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
        return _list_to_2D(bubble_list, config)

def test():
    output = generate_level(1,1, required=['netherlands'], only_required=True)
    for row in output:
        test_string = " ".join(map(str, row))
        print(test_string.center(20))
    print("Done!")

test()