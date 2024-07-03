from dataclasses import dataclass

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


DESIGNS = [ # These are based on default field width and height
    DesignElement(name = 'torii', cost = 6, chance_weight = 1, treat_as_fill = True,
                  output = [2, 0, 0, 0, 0, 0, 0, 2, 
                             2, 2, 2, 2, 2, 2, 2, 
                            0, 0, 2, 0, 0, 2, 0, 0, 
                             0, 2, 2, 2, 2, 2, 0, 
                            0, 2, 0, 0, 0, 0 ,2, 0, 
                             2, 0, 0, 0, 0, 0, 2]),
    DesignElement(name = 'fireworks', cost = 3, chance_weight= 1,
                  output = [[0, 24, 24],
                             [24, 97, 24],]),    
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