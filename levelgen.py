from dataclasses import dataclass

from consts import DESIGNS, FILLS
from helpers import _apply_element, _apply_fill, _filter_list, _list_to_2D, \
    _list_to_string, _weighted_roll, _2d_to_list


@dataclass
class GeneratorConfig:
    """Configuration data for the level generator.
    
    Parameters
    ----------
    base_difficulty : int
        gets multiplied with the world number to reach a starting difficulty
    diff_per_level : int
        difficulty added per level
    diff_per_star : int
        difficulty per star
    minimum_difficulty : int
        minimum difficulty for the generation, will be used if calculated difficulty is lower
    field_width : int
        the maximum number of bubbles in your top row
    field_height : int
        the maximum number of rows in your playing field
    return_string : bool, optional
        a flag used to return the output as one single string instead for compatibility reasons (default = False)
    """
    base_difficulty: int = 20
    diff_per_level: int = 1
    diff_per_star: int = 1
    minimum_difficulty: int = 40
    field_width: int = 8
    field_height: int = 8
    return_string: bool = False


def generate_level(
            world, level, stars=0,  required=[], excludes=[],
            elements_set=DESIGNS, fill_set=FILLS, config=GeneratorConfig(),
            only_required=False):
    """Generate a level based on the provided designs and parameters.
    
    Generates a 2d Array or string that contains all of the integers for the level .JSON-file 
    based on entered config parameters, element and fill arrays.

    Parameters
    ----------
    world : int
        the number of the world, used to determine difficulty
    level : int
        the number of the level, used to determine difficulty
    stars : int, optional
        the number of stars required to unlock the level, used to determine difficulty (default is 0)
    required : list, optional
        a list of additional requirements for the method, this can be int for colors, and string for names or keywords (default is empty)
    excludes : list, optional
        a list of things to exclude from the generation, this can be int for colors, and string for names or keywords (default is empty)
    elements_set : list, optional
        the list of DesignElements to incorporate (default is DESIGNS from consts.py)
    fill_set : list, optional
        the list of Fills to incorporate (default is FILLS from consts.py)
    config : GeneratorConfig, optional
        the configuration for this function (default is a default GeneratorConfig)
    only_required : bool, optional
        a flag used to make the function only use the specified requirements and no additions (default is False)
    """

    # Get total difficulty to spend on this level.
    level_difficulty = (config.base_difficulty * world
                        + config.diff_per_level * level 
                        + config.diff_per_star * stars)
    if level_difficulty <= config.minimum_difficulty:
        level_difficulty = config.minimum_difficulty
    spent_difficulty = 0

    # Make bubble list, due to the nature of hex grids, 
    # the field has a base width at even height numbers, 
    # and width-1 at odd numbers.
    bubble_list = []
    for height in range(0, config.field_height):
        if height % 2 == 0:
            bubble_list += ([0] * config.field_width)
        else:
            bubble_list += ([0] * (config.field_width-1))

    # Select a fill either based on a pre-defined name 
    # or from the constant, filtered or not.
    fills_to_roll = []
    selected_fill = None

    # See if we have a fill defined. 
    # We can only use one fill, so we stop as soon as we find one pre-defined.
    for fill in fill_set:
        if fill.name in required:
            selected_fill = fill
            break
    
    # If we have no pre-defined fills, filter the list of fills 
    # using the excluding keywords, and roll on the result.
    if selected_fill is None:
        fills_to_roll = _filter_list(excludes, fill_set)
        selected_fill = _weighted_roll(fills_to_roll)
    spent_difficulty += selected_fill.cost

    # Take the required names and queue all elements that are predefined, then apply them.
    queued_elements = []
    for element in elements_set:
        if element.name in required:
            spent_difficulty += element.cost
            queued_elements.append(element)

    # Roll design elements and add the cost to what we have spent.
    elements_to_roll = _filter_list(excludes, elements_set)
    while spent_difficulty < level_difficulty and not only_required:
        selected_element = _weighted_roll(elements_to_roll)
        spent_difficulty += selected_element.cost
        queued_elements.append(element)
    
    # Apply all of the queued elements.
    for element in queued_elements:
        if element.treat_as_fill:
            bubble_list = _apply_fill(element, bubble_list, config)
        else:
            bubble_list = _apply_element(element, bubble_list, config)

    # Apply the fill to our level
    bubble_list = _apply_fill(selected_fill, bubble_list, excludes, required, config)

    if config.return_string: # Give output as one string.
        return _list_to_string(bubble_list)
    else: # Give output as 2D List.
        return _list_to_2D(bubble_list, config)


_2d_to_list(DESIGNS[5], GeneratorConfig())