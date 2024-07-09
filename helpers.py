import random

def _apply_element(element, list, config):
    """Applies the output of an element to the list of bubbles."""
    list_to_return = list
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
    
    # Apply the design, row by row.
    for row in element.output:
        for bubble in row:

            if element.override == True or list_to_return[index] == 0:
                if bubble != 0:
                    list_to_return[index] = bubble
            index += 1
        
        # Move to the next row.
        index, is_odd_row = _jump_row(index, row, is_odd_row, config)
        
    return list_to_return

def _apply_fill(fill, list, excludes, required, config):
    """Applies the output of a fill to the list of bubbles and returns the new list."""
    list_to_return = list
    fill_to_apply = _color_swap(fill, _filter_colors(list, 4, excludes), required)

    # Overwrite any empty spaces with the fill or just overwrite anything with override=True.
    for index in range(len(fill_to_apply)):
        if fill.override == True or list_to_return[index] == 0:
            if fill_to_apply[index] != 0:
                list_to_return[index] = int(fill_to_apply[index])

    return list_to_return

def _color_swap(element, color_list, required):
    """Swaps string color variables to integers."""
    list_to_return = []
    required_colors = []
    color_dict = {}

    # Add any required colors to their own list
    for entry in required:
        if isinstance(entry, int):
            required_colors.append(entry)

    # Go through the output and replace strings with integers. Takes any required colors first.
    for entry in element.output:
        if isinstance(entry, str):
            if entry not in color_dict:
                if len(required_colors) != 0:
                    color_dict[entry] = required_colors.pop(0)
                    if color_dict[entry] in color_list:
                        color_list.remove(color_dict[entry])
                else:
                    color_dict[entry] = color_list.pop(random.randint(0, len(color_list)-1))

        if entry in color_dict:
            list_to_return.append(color_dict[entry])
        else:
            list_to_return.append(entry)
    return list_to_return

def _filter_colors(bubble_list, min_colors, excludes):
    """Takes the range of basic color ints and removes the ones in use. Will then pad the range with random ints if there would not be enough colors in the list."""
    colors_to_return = []
    for number in range(1,10):
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
        colors_to_return.append(random.randint(1,9))

    return colors_to_return

def _filter_list(excludes, list_to_filter):
    """Filters a list based on provided keywords or names and returns the list without those matches."""
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
    """Picks a random legal starting location on the grid and returns the starting index and if this is on an odd/even row."""
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
        x_axis = random.randint(x_start, config.field_width - (widest_row_width+1)) # Adding the 1 means it doesn't accidentally cut off the next row.
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

def _get_widest(output):
    """Returns the length of the widest row in the output."""
    widest_row = []
    for row in output:
        if len(row) > len(widest_row):
            widest_row = row
    return len(widest_row)

def _jump_row(index, row, is_odd_row, config):
    """Skips to the next row."""
    if is_odd_row:
        index += (config.field_width - len(row)-1)
        is_odd_row = False
    else:
        index += (config.field_width - len(row))
        is_odd_row = True
    return index, is_odd_row

def _list_to_2D(list, config):
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

def _verify_legal_placement(element, list, config, index, is_odd_row):
    """Makes sure the selected element can legally be placed completely in the selected area."""
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