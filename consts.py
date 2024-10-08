from dataclasses import dataclass, field

@dataclass
class DesignElement:
    """Level Design Element that provides a string that can be loaded onto the list of bubbles.

    If treat_as_fill is True, make sure to provide an output that will run from the first bubble.
    If not, provide the output in a 2D list with a list per row. Remember to use leading zeroes in your designs when needed.

    Parameters
    ----------
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
          maximum starting point for the design element, allows you to better position elements (default = 0)
     treat_as_fill : bool, optional
          a flag used to determine whether to use the apply fill method rather than the apply element method
          if True, make sure to supply a fill as single long list that spans your playing field (default = False)
     allowed_colors: list[int], optional
          a list of valid choices for when the design uses letter variables. If provided as [], it will pick a random
          color instead (default = [])
     override : bool, optional
          a flag used to make the element overwrite any existing bubbles (default = False)
    """
    name: str
    cost: int
    chance_weight: int
    keywords: list
    output: list
    y_min: int = 0
    y_max: int = 0
    treat_as_fill: bool = False
    allowed_colors: list[int] = field(default_factory=list)
    override: bool = False

@dataclass
class Fill:
    """Level Design Fill that is used to fill in the spaces between design elements after generation.

    Parameters
    ----------
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
    """
    name: str
    cost: int
    chance_weight: int
    output: list
    keywords: list
    override: bool = False


DESIGNS = [ # These are based on default field width and height
     DesignElement(name = 'torii', cost = 20, chance_weight = 1, treat_as_fill = True,
          keywords = ['fill', 'japan'],
          output = [
               0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0,
               2, 0, 0, 0, 0, 0, 0, 2, 
               2, 2, 2, 2, 2, 2, 2, 
               0, 0, 2, 0, 0, 2, 0, 0, 
               0, 2, 2, 2, 2, 2, 0, 
               0, 2, 0, 0, 0, 0 ,2, 0, 
               2, 0, 0, 0, 0, 0, 2,
               ]),
     DesignElement(name = 'fireworks', cost = 15, chance_weight = 3, y_max = 1,
          allowed_colors=[21, 22, 23, 24, 25, 26, 27, 28, 29], keywords = ['locked'],
          output = [
               [0, 'A', 'A'],
               ['A', 97, 'A'],
               ]),
     DesignElement(name = 'cloud', cost = 10, chance_weight = 5, y_max = 1,
          keywords = [],
          output = [
               [0, 7, 7],
               [7, 7, 7],
               ]),
     DesignElement(name = 'cloudJP', cost = 10, chance_weight = 5, y_max = 1,
          keywords = ['japan'],
          output = [
               [7, 7, 7, 7, 0],
               [0, 0, 7, 0, 0],
               [0, 7, 7, 7, 7],
               ]),
     DesignElement(name = 'cherrytree', cost = 30, chance_weight = 1,
          keywords = ['japan'],
          output = [
               [0, 5, 5],
               [5, 5, 5],
               [5, 1, 1, 0],
               [0, 1, 5, 0],
               [0, 1, 1, 0, 0],
               [0, 1, 0, 0, 0],
               ]),
     DesignElement(name = 'pinetree', cost = 30, chance_weight = 1,
          keywords = [],
          output = [
               [0, 0, 9],
               [9, 9],
               [9, 9, 9],
               [9, 9, 9, 9],
               [0, 0, 1, 0, 0],
               [1, 1, 0, 0],
               ]),
     DesignElement(name = 'tree', cost = 30, chance_weight = 1,
          keywords = [],
          output = [
               [0, 9, 9],
               [9, 9, 9],
               [9, 1, 9, 9],
               [0, 1, 9, 0],
               [1, 1, 0, 0],
               [1, 0, 0, 0],
               [1, 1, 0, 0, 0],
               ]),
     DesignElement(name = 'mountain', cost = 60, chance_weight = 1, treat_as_fill = True,
          keywords = ['fill', 'japan'],
          output = [
               0, 0, 0, 2, 2, 0, 0, 0,
               0, 0, 2, 7, 2, 0, 0,
               0, 0, 0, 7, 7, 0, 0, 0, 
               0, 0, 8, 7, 8, 0, 0, 
               0, 0, 8, 8, 8, 8, 0, 0, 
               0, 8, 8, 8, 8, 8, 0, 
               0, 8, 8, 8, 8, 8 ,8, 0, 
               8, 8, 8, 8, 8, 8, 8,
               ]),
     DesignElement(name = 'bridge', cost = 20, chance_weight = 1, treat_as_fill = True,
          keywords = ['fill'],
          output = [
               0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 
               0, 0, 0, 0, 0, 0, 0, 
               0, 7, 0, 0, 0, 0, 7, 0, 
               8, 8, 8, 8, 8, 8, 8, 
               7, 7, 0, 0, 0, 0, 7, 7, 
               7, 0, 0, 0, 0, 0, 7,
               ]),
     DesignElement(name = 'windmill', cost = 40, chance_weight = 1,
          keywords = ['ned'],
          output = [
               [7, 0, 0, 7],
               [7, 1, 7, 0],
               [3, 3, 0, 0],
               [7, 1, 7, 0, 0],
               [7, 1, 1, 7, 0, 0],
               ]), 
     DesignElement(name = 'triangle_down_large', cost = 10, chance_weight = 5,
          keywords = [],
          output = [
               ['A', 'A', 'A'],
               ['A', 'A', 0],
               ['A', 0, 0],
               ]),
     DesignElement(name = 'triangle_down_small', cost = 5, chance_weight = 5,
          keywords = [],
          output = [
               ['A', 'A'],
               ['A', 0],
               ]),
     DesignElement(name = 'triangle_up_large', cost = 10, chance_weight = 5,
          keywords = [],
          output = [
               [0, 0, 'A'],
               ['A', 'A'],
               ['A', 'A', 'A'],
               ]),
     DesignElement(name = 'triangle_up_small', cost = 5, chance_weight = 5,
          keywords = [],
          output = [
               [0, 'A'],
               ['A', 'A'],
               ]),
     DesignElement(name = 'diamond_small', cost = 5, chance_weight = 5,
          keywords = [],
          output = [
               [0, 'A'],
               ['A', 'A'],
               ['A', 0],
               ]),
     DesignElement(name = 'diamond_large', cost = 5, chance_weight = 5,
          keywords = [],
          output = [
               [0, 'A'],
               ['A', 'A'],
               ['A', 'A', 'A'],
               ['A', 'A', 0],
               ['A', 0, 0],
               ]),
     DesignElement(name = 'circle', cost = 5, chance_weight = 5,
          keywords = [],
          output = [
               [0, 'A', 'A'],
               ['A', 'A', 'A'],
               ['A', 'A', 0],
               ]),
]

FILLS = [   # These are based on default field width and height
     Fill(name = 'ireland', cost = 10, chance_weight = 1, 
          keywords = ['flag', 'ire'],
          output = [
               9, 9, 7, 7, 7, 7, 3, 3,
               9, 9, 7, 7, 7, 3, 3,
               9, 9, 7, 7, 7, 7, 3, 3,
               9, 9, 7, 7, 7, 3, 3,
               9, 9, 7, 7, 7, 7, 3, 3,
               9, 9, 7, 7, 7, 3, 3,
               9, 9, 7, 7, 7, 7, 3, 3,
               ]),
     Fill(name = 'netherlands', cost = 10, chance_weight = 1, 
          keywords = ['flag', 'ned'],
          output = [
               2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2,
               7, 7, 7, 7, 7, 7, 7, 7,
               7, 7, 7, 7, 7, 7, 7,
               6, 6, 6, 6, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6,
               0, 0, 0, 0, 0, 0, 0, 0,
               ]),
     Fill(name = 'japan', cost = 10, chance_weight = 1, 
          keywords = ['flag', 'japan'],
          output = [
               7, 7, 7, 7, 7, 7, 7, 7,
               7, 7, 7, 7, 7, 7, 7,
               7, 7, 7, 2, 2, 7, 7, 7,
               7, 7, 2, 2, 2, 7, 7,
               7, 7, 7, 2, 2, 7, 7, 7,
               7, 7, 7, 7, 7, 7, 7,
               7, 7, 7, 7, 7, 7, 7, 7,
               ]),
     Fill(name = 'ustates', cost = 10, chance_weight = 1, 
          keywords = ['flag', 'usa'],
          output = [
               7, 6, 6, 2, 2, 2, 2, 2,
               6, 2, 6, 7, 7, 7, 7,
               6, 6, 6, 2, 2, 2, 2, 2,
               7, 7, 7, 7, 7, 7, 7,
               2, 2, 2, 2, 2, 2, 2, 2,
               0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0,
               ]),
     Fill(name = 'australia', cost = 10, chance_weight = 1, 
          keywords = ['flag', 'aus'],
          output = [
               2, 6, 2, 6, 6, 6, 6, 6,
               2, 2, 6, 6, 7, 6, 6,
               2, 6, 2, 6, 6, 6, 7, 6,
               6, 6, 6, 7, 6, 7, 6,
               6, 7, 7, 6, 6, 6, 6, 6,
               6, 7, 6, 6, 7, 6, 6,
               6, 6, 6, 6, 6, 6, 6, 6,
               ]),
     Fill(name = 'skyground', cost = 10, chance_weight = 4, 
          keywords = ['day', 'night'],
          output = [
               6, 6, 6, 6, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6, 6,
               1, 1, 1, 1, 1, 1, 1,
               8, 8, 8, 8, 8, 8, 8, 8,
               0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0,
               ]),
     Fill(name = 'skygroundDUSK', cost = 10, chance_weight = 4, 
          keywords = ['dusk'],
          output = [
               3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3, 3,
               1, 1, 1, 1, 1, 1, 1,
               8, 8, 8, 8, 8, 8, 8, 8,
               0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0,
               ]),
     Fill(name = 'city', cost = 30, chance_weight = 4, 
          keywords = [],
          output = [
               6, 6, 6, 6, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6,
               6, 8, 6, 6, 6, 6, 8, 8,
               8, 8, 6, 8, 6, 8, 8,
               8, 8, 0, 8, 0, 0, 8, 8,
               8, 8, 0, 8, 0, 8, 8,
               0, 0, 0, 0, 0, 0, 0, 0,
               ]),
     Fill(name = 'frame', cost = 40, chance_weight = 4, override = True, 
          keywords = ['museum'],
          output = [
               1, 1, 1, 8, 8, 1, 1, 1,
               1, 0, 0, 0, 0, 0, 1,
               1, 0, 0, 0, 0, 0, 0, 1,
               8, 0, 0, 0, 0, 0, 8,
               8, 0, 0, 0, 0, 0, 0, 8,
               1, 0, 0, 0, 0, 0, 1,
               1, 0, 0, 0, 0, 0, 0, 1,
               1, 1, 8, 8, 8, 1, 1,
               ]),
     # Name goes 'diagonal[Direction (L/R)][number of colors]'
     Fill(name = 'diagonalR2', cost = 30, chance_weight = 4, 
          keywords = ['diagonal'],
          output = [
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'B', 'A', 'B', 'A', 'B', 'A', 'B',
               ]),
     Fill(name = 'diagonalR3', cost = 30, chance_weight = 4,
          keywords = ['diagonal'],
          output = [
               'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A',
               'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A',
               'C', 'A', 'B', 'C', 'A', 'B', 'C',
               'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C',
               'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A',
               ]),
     Fill(name = 'diagonalR4', cost = 30, chance_weight = 4, 
          keywords = ['diagonal'],
          output = [
               'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D', 'A', 'B', 'C',
               'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C',
               'D', 'A', 'B', 'C', 'D', 'A', 'B',
               'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B',
               'C', 'D', 'A', 'B', 'C', 'D', 'A',
               'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A',
               'B', 'C', 'D', 'A', 'B', 'C', 'D',
               ]),
     Fill(name = 'diagonalL2', cost = 30, chance_weight = 4,
          keywords = ['diagonal'],
          output = [
               'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'B', 'A', 'B', 'A', 'B', 'A', 'B',
               ]),
     Fill(name = 'diagonalL3', cost = 30, chance_weight = 4,
          keywords = ['diagonal'],
          output = [
               'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A',
               'A', 'C', 'B', 'A', 'C', 'B', 'A',
               'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C',
               'C', 'B', 'A', 'C', 'B', 'A', 'C',
               'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B',
               'B', 'A', 'C', 'B', 'A', 'C', 'B',
               'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A',
               'A', 'C', 'B', 'A', 'C', 'B', 'A',
               ]),
     Fill(name = 'diagonalL4', cost = 30, chance_weight = 4,
          keywords = ['diagonal'],
          output = [
               'D', 'C', 'B', 'A', 'D', 'C', 'B', 'A',
               'C', 'B', 'A', 'D', 'C', 'B', 'A',
               'C', 'B', 'A', 'D', 'C', 'B', 'A', 'D',
               'B', 'A', 'D', 'C', 'B', 'A', 'D',
               'B', 'A', 'D', 'C', 'B', 'A', 'D', 'C',
               'A', 'D', 'C', 'B', 'A', 'D', 'C',
               'A', 'D', 'C', 'B', 'A', 'D', 'C', 'B',
               'D', 'C', 'B', 'A', 'D', 'C', 'B',
               ]),
     Fill(name = 'columns2narrow', cost = 30, chance_weight = 4,
          keywords = ['column'],
          output = [
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
               'A', 'B', 'A', 'B', 'A', 'B', 'A',
               ]),
     Fill(name = 'columns2broad', cost = 30, chance_weight = 4,
          keywords = ['column'],
          output = [
               'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B',
               'A', 'A', 'B', 'B', 'A', 'A', 'B',
               ]),
     Fill(name = 'columns3', cost = 30, chance_weight = 4,
          keywords = ['column'],
          output = [
               'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A',
               'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A',
               'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A',
               'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
               'A', 'B', 'C', 'A', 'B', 'C', 'A',
               ]),
     Fill(name = 'columns4', cost = 30, chance_weight = 4,
          keywords = ['column'],
          output = [
               'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D', 'A', 'B', 'C',
               'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D', 'A', 'B', 'C',
               'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D', 'A', 'B', 'C',
               'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D', 'A', 'B', 'C',
               ]),
]