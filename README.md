# bubble-levelgen
 Level Generation Code for Bubble Shooter Games

## Description
This code generates bubble grids for Bubble Shooter games. 
Each level is built up from a number of Designs and a Fill, which we'll call 'elements'.
Elements are selected through a weighted roll, and 'cost' difficulty. The program keeps applying elements until the alloted difficulty - decided through arguments - is 'spent'.
Additional parameters for elements and the function allow for more control over the output by filtering or queueing elements.
The output is intended to be used in your own game.

![Screenshot of an example level in the bubble shooter game this code is inisially designed for.](/assets/example.jpg)

## Installation
This is intended to be used as a module or package. Add the file to the folder with your other modules and import it in your program.

`from levelgen import generate_level`

You can also import the dataclasses for your own use (see Data Classes below):
    from consts import Fill, DesignElement
    from levelgen import GeneratorConfig
You may wish to do this if:
- your playing field is not 8x8,
- you wish to supply your own designs,
- or you wish to make edits to the configuration.

## Execution and Usage
The generate_level() function returns a 2D List* containing the generated level. 
At it's most basic use, the function takes two arguments: the world number and level number, like so:

`new_level = generate_level(1,2)`

The function can take many other arguments, however, which will allow you to control its output, for example:

    newer_level = generate_level(1,2, 
        required=[1, 2, 'diagonalR2'], 
        only_required=True)

See the 'examples.py' file for more examples as well as a test function that provides an easier to read output.
It is recommended to combine this code with a spreadsheet or other method of organising your input.
You can then take the generated level and store it in a .JSON-file for use in your own game, for instance.

*There is a configuration option to return one String instead for compatiblity with available older projects such as [this bubble shooter project](https://github.com/tastelikecoke/shoot-bubble).

## Parameters
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

## Data Classes
This module makes use of three different dataclasses, which together make up all of the customization and configuration of the module. The module comes with a default set of each, but it is recommended to provide your own if you are using a playing field that is not 8x8 bubbles.

### GeneratorConfig
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

### DesignElement
    name : str
        element name - make sure this is unique
    cost : int
        difficulty cost
    chance_weight : int
        how much this element is weighted in determining which elements to pick
    keywords: list
        a list of strings that can be used to filter out the element from the available elements
    output : list
        the bubbles of which the design element consists
    y_min : int, optional
        minimal starting point for the design element, allows you to better position elements (default = 0)
    y_max : int, optional
        maximum starting point for the design element, allows you to better position elements, is ignored at 0 (default = 0)
    treat_as_fill : bool, optional
        a flag used to determine whether to use the apply fill method rather than the apply element method
        if True, make sure to supply a fill as single long list that spans your playing field (default = False)
    allowed_colors: list[int], optional
        a list of valid choices for when the design uses letter variables. If provided as [], it will pick a random
        color instead (default = [])
    override : bool, optional
        a flag used to make the element overwrite any existing bubbles (default = False)

### Fill
A special element that is used to fill up the playing field after other elements have been placed.

    name : str 
        fill name, make sure this is unique
    cost : int
        base difficulty cost
    chance_weight : int
        how much this element is weighted in determining which fill to pick
    output : list
        the bubbles of which the fill consists
    keywords : list
        a list of strings that can be used to filter out the fill from the available fills
    override : bool, optional 
        a flag used to make the fill overwrite any existing bubbles (default = False)

## Bubble Legend
    0 - Blank/Empty
    1 - Brown
    2 - Red
    3 - Orange
    4 - Yellow
    5 - Pink
    6 - Blue
    7 - White
    8 - Gray
    9 - Green
    10-19 - Unused
    20 - Wild
    21-39 - Locked versions of 1-19
    97 - Explosion
    98 - Fireworks Unlock
    99 - Fireworks Launcher
Note: this bubble legend is based off of the project for which this code is written and is used for all the elements provided.

## Current Features
- Generates levels for Bubble Shooters based on provided Designs and Fills.
- Comes with a set of 10 Design Elements and 19 Fills.
- Designs can be supplied with a variety of arguments, such as:
-- whether to treat it as a 2D list or as a Fill,
-- minimum and maximum position on the y-axis,
-- and whether to override previously placed elements.
- Fills are lists that span the bubble grid and can take letter strings, e.g. 'A', as variables.
- Exclusions can filter elements based on name, keywords, or color content.
- Requirements can ensure specific elements, as well as specific colors for letter string variables.
- Outputs bubble grid as 2D List*.

*Can also output a String, but this is mainly intended for compatibility or testing rather than actual use.

## Change Log
### v1.1 - Letter Variables for Design Elements
- Added ability to use strings as variables in Design Elements.
- Added 7 new basic Design Elements that use strings as part of their output.
- Edited 'fireworks' Design Element to use strings.
- Added new minimum difficulty to GeneratorConfig to help alleviate generation issues in low difficulties.
  - Minimum difficulty will be used instead of calculated difficulty if the latter is lower.


### v1.0 - First Release
- Initial release.

## Author's Info