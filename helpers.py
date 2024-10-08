import random
import dataclasses

def _apply_element(element, list, config):
    """Apply the output of an element to the list of bubbles."""
    list_to_return = list
    # We use an empty list in the required section as that is used for fills;
    # for elements we use the allowed_colors section instead.
    
    index = 0
    is_odd_row = True
    attempts = 0
    is_legal = False

    # Try to find a starting location a few times before giving up.
    while not is_legal:
        # If we have tried too often, just give up.
        if attempts > 5:
            return list_to_return
        # Otherwise, pick a starting location and see if we're allowed to place there.
        else:
            index, is_odd_row = _get_starting_index(element, config)
            is_legal = _verify_legal_placement(element, list, config, index, is_odd_row)

        attempts +=1
    
    element_to_apply = _2d_to_list(_color_swap_element(element), config)

    for bubble in element_to_apply:
        try:
            if element.override == True or list_to_return[index] == 0:
                if bubble != 0:
                    list_to_return[index] = bubble
        except:
            pass
        index += 1
        
    return list_to_return

def _apply_fill(fill, list, excludes, required, config):
    """Apply the output of a fill to the list of bubbles and return the new list."""
    list_to_return = list
    fill_to_apply = _color_swap_fill(fill, _filter_colors(list, 4, excludes), required)

    # Overwrite any empty spaces with the fill or just overwrite anything with override=True.
    for index in range(len(fill_to_apply)):
        if fill.override == True or list_to_return[index] == 0:
            if fill_to_apply[index] != 0:
                list_to_return[index] = int(fill_to_apply[index])

    return list_to_return

def _color_swap_element(element):
    """Swap string color variables in elements to integers."""
    list_to_return = []
    color_dict = {}
    allowed_colors = element.allowed_colors.copy()
    element_to_return = dataclasses.replace(element)

    # Populate the allowed color list with the standard 1-9 color ints if we did
    # not specify any specific allowed colors.
    if len(allowed_colors) == 0:
        for number in range(1, 10):
            allowed_colors.append(number)

    for row in element.output:
        row_to_append = []
        for bubble in row:
            if isinstance(bubble, str):
                if bubble not in color_dict:
                    color_dict[bubble] = allowed_colors.pop(random.randint(0, len(allowed_colors) - 1))

            if bubble in color_dict:
                row_to_append.append(color_dict[bubble])
            else:
                row_to_append.append(bubble)

        list_to_return.append(row_to_append)

    element_to_return.output = list_to_return
    return element_to_return

def _color_swap_fill(element, color_list, required):
    """Swap string color variables in fills to integers."""
    list_to_return = []
    required_colors = []
    color_dict = {}

    # Add any required colors to their own list
    for entry in required:
        if isinstance(entry, int):
            required_colors.append(entry)

    # Go through the output and replace strings with integers. 
    # Takes any required colors first.
    for entry in element.output:
        if isinstance(entry, str):
            if entry not in color_dict:
                if len(required_colors) != 0:
                    color_dict[entry] = required_colors.pop(0)
                    if color_dict[entry] in color_list:
                        color_list.remove(color_dict[entry])
                else:
                    color_dict[entry] = color_list.pop(random.randint(0, len(color_list) - 1))

        if entry in color_dict:
            list_to_return.append(color_dict[entry])
        else:
            list_to_return.append(entry)
    return list_to_return

def _filter_colors(bubble_list, min_colors, excludes):
    """Take the range of basic color ints and remove the ones in use. Then pad the range with random ints if there would not be enough colors."""
    colors_to_return = []
    for number in range(1, 10):
        colors_to_return.append(number)
    
    # Filter out all of the used integers
    for bubble in bubble_list:
        if bubble in colors_to_return:
            colors_to_return.remove(bubble)
    
    # Filter out all excluded integers
    for entry in excludes:
        if entry in colors_to_return:
            colors_to_return.remove(entry)
    
    # If not enough colors to satisfy the min_colors, add random colors until we do.
    while len(colors_to_return) < min_colors:
        colors_to_return.append(random.randint(1, 9))

    return colors_to_return

def _filter_list(excludes, list_to_filter):
    """Filter a list based on provided keywords or names and return the list without those matches."""
    filtered_list = []
    for entry in list_to_filter:
        add_to_list = True

        # Filter based on name or keywords.
        if entry.name not in excludes:
            for keyword in entry.keywords:
                if keyword in excludes:
                    add_to_list = False
        else:
            add_to_list = False
        
        # Filter based on color integers.
        if isinstance(entry.output[0], list): # This is a multi-list output like Design Elements.
            for row in entry.output:
                for bubble in row:
                    if bubble in excludes:
                        add_to_list = False
        else: # This is a Fill or a Design Element treated as Fill.
            for bubble in entry.output:
                if bubble in excludes:
                    add_to_list = False

        if add_to_list:
                filtered_list.append(entry)

    return filtered_list

def _get_starting_index(element, config):
    """Pick a random legal starting location on the grid and return the starting index and if this is an odd or even row."""
    starting_index = 0
    widest_row_width = _get_widest(element.output)
    
    # Pick a random starting location on the playing field.
    # Make sure the entire design fits on the field height-wise.
    y_axis = 0
    if element.y_max != 0:
        y_axis = random.randint(element.y_min, element.y_max)
    else:
        y_axis = random.randint(element.y_min, config.field_height - len(element.output))

    # Make it so that we don't cut off the element by accident.
    x_start = widest_row_width - len(element.output[0])

    # Get correct x_axis offset depending on which row we start on.
    if y_axis % 2 == 0: 
        # Adding the 1 prevents it from accidentally cutting off the next row.
        try:
            x_axis = random.randint(x_start, config.field_width - (widest_row_width + 1))
        except:
            x_axis = random.randint(0, 1)
        is_odd_row = False
    else:
        x_axis = random.randint(x_start, (config.field_width - 1) - widest_row_width)
        is_odd_row = True
    
    # Set starting bubble index, starting with the correct row.
    for row_nr in range(0, y_axis):
        if row_nr % 2 == 0:
            starting_index += config.field_width
        else:
            starting_index += config.field_width - 1

    # Now move to the correct column.
    starting_index += x_axis
    return starting_index, is_odd_row

def _get_widest(output):
    """Return the length of the widest row in the output."""
    widest_row = []
    for row in output:
        if len(row) > len(widest_row):
            widest_row = row
    return len(widest_row)

def _2d_to_list(element, config):
    output_to_return = []
    field_width = config.field_width

    # Go through the rows in the output; we use a non-pythonic solution so we can 
    # easily access the length of the next row.
    for index in range(0, len(element.output)):
        # Append all of the bubbles and then apply a number of 0's to reach the
        # starting point of the next row.
        for bubble in element.output[index]:
            output_to_return.append(bubble)
        try:
            for i in range(0, field_width - len(element.output[index+1])):
                output_to_return.append(0)
        except:
            pass

        #is_odd_row = not is_odd_row

    return output_to_return

def _jump_row(index, row, is_odd_row, config):
    """Skip to the next row."""
    filled_bubbles = 0
    for bubble in row:
        if bubble == 0:
            pass
        else:
            filled_bubbles = filled_bubbles + 1

    index += (config.field_width - 1 - filled_bubbles)
    is_odd_row = not is_odd_row
    return index, is_odd_row

def _list_to_2D(list, config):
    """Change the bubble list input to a 2D List to return."""
    list_to_return = []

    for index in range(0, config.field_height):
        temp_list = []
        if index % 2 == 0:
            for i in range(0, config.field_width):
                temp_list.append(list.pop(0))
        else:
            for i in range(0, config.field_width - 1):
                temp_list.append(list.pop(0))
        list_to_return.append(temp_list)
        
    return list_to_return

def _list_to_string(list):
    """Change the bubble list input to a string to return."""
    string_to_return = ''

    for entry in list:
        string_to_return += str(entry)
    
    return string_to_return

def _verify_legal_placement(element, list, config, index, is_odd_row):
    """Make sure the selected element can legally be placed completely in the selected area."""
    # If the element is set to override, any placement is legal!
    if element.override == True:
        return True
    else:
        # Trawl through the list starting from the selected point
        current_index = index

        for row in element.output:
            for bubble in row:
                if list[index] == 0:
                    current_index += 1
                else:
                    return False
            
        index, is_odd_row = _jump_row(current_index, row, is_odd_row, config)
        
        # No issues found!
        return True
    
def _weighted_roll(elements_set):
    """Return a random index from a list with items with weighted chances."""
    # Ensure we always at least return a random element.
    element_to_return = random.choice(elements_set)

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
            element_to_return = element
        
    return element_to_return