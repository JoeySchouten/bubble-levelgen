# bubble-levelgen
 Level Generation Code for Bubble Shooter Games

## Description
-What do
-How do
-What makes a level hard?

## Installation
This is a .py-file intended to be used as a module. Add the file to the folder with your other modules and import it in your program.
    from levelgen import generate_level

## Execution and Usage
The generate_level() function returns either a 2D List or a String containing the generated level. 
At it's most basic use, the function takes two arguments: the world number and level number, like so:

`new_level = generate_level(1,2)`

You can then take that output and use it in your game. The higher your world and level numbers, the more difficulty the function gets to 'spend', and as a result your level should be harder. Since the module comes with its own configuration and sets of design elements and fills, this is all you technically need if you use a 9x8 playing field.

The function can take a lot more arguments, however, allowing you to customize it to work with your own designs, level of difficulty, and your own playing field size.

`generate_level(world, level, stars=0, config=GeneratorConfig(), elements_set=DESIGNS, fill_set=FILLS, return_string=False)`

Let's go over these arguments one by one and unpack them.

### World (int)
This is the world number - the idea being that each next world is more difficult than the last. Think of it as in the old Mario game: Level 3-1 should be harder than Level 1-1.

### Level (int)
This is the level number - as with the world number, each level gets more difficult as you go along. This should be a smaller step than between worlds.

### Stars (int) default = 0
The number of stars the player needs to have by the time they get to the level. Some games allow players to unlock levels by collecting stars or medals for their score, which can also be used as an indication of difficulty. A level that requires 10 stars to unlock should be easier than one that requires 100.

### Config (GeneratorConfig) default = GeneratorConfig()
This is where the configuration for the generator goes. This dataclass contains the most basic levers for the generator and contains your playing field size as well as how the difficulty scales. If not specified, it just takes the default version specified in the module. See more in the 'Data Classes' section below.

### Element Set (List\[DesignElements\]) default = DESIGNS
This is the list of Design Elements that the generator will pick from to populate the playing field. The module contains a default set of elements. See more in the 'Data Classes' section below.

### Fill Set (List\[Fill\]) default = FILLS
This is the list of Fills that the generator will pick from to fill in remaining spaces in the playing field after placing all Design Elements. The module contains a default set of fills. See more in the 'Data Classes' section below.

### Return String (bool) default = False
Whether the method returns the output as a 2D List (False) or as a single string (True). Generally you want to use the 2D List for easier use in your own project. However, if you use the single string method, it is compatible with available projects such as [this bubble shooter project](https://github.com/tastelikecoke/shoot-bubble).

## Data Classes
This module makes use of three different dataclasses, which together make up all of the customization and configuration of the module. The module comes with a default set of each, but it is recommended to provide your own if you are using a playing field that is not 9x8 bubbles.

### GeneratorConfig
Mainly detemrines the playing field size and difficulty scaling across levels.
    base_difficulty: int - Starting difficulty; gets multiplied with the world number to reach a base difficulty for each world.
    diff_per_level: int - Difficulty added per level.
    diff_per_star: int - Difficulty per star.
    field_width: int - The maximum number of bubbles in your top row.
    field_height: int - The maximum number of rows in your playing field.

### DesignElement
    name: str - Element name, make sure this is unique.
    cost: int - Base difficulty cost.
    chance_weight: int - How much this element is weighted in determining which elements to pick.
    output: str - The bubbles the design element consists of.
    override: bool - Whether the design element overwrites any existing bubbles. Default = True.

### Fill
    name: str - Element name, make sure this is unique.
    cost: int - Base difficulty cost.
    chance_weight: int - How much this element is weighted in determining which fill to pick.
    output: str - The bubbles the fill consists of.
    override: bool  - Whether the fill overwrites any existing bubbles. Default = False.

## Current Features
## Change Log
## Author's Info