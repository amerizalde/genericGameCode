import bpy, math

"""
- Assign a height value (float) to each corner of the rectangle.
- Divide the rectangle into 4 sub-rectangles.
- Let their height value be the mean values of the corners of the parent rectangle.
- When calculating the common point of the 4 sub rectangles, introduce a small error
into the calculation to achieve roughness.
- Iterate and subdivide each rectangle into 4 sub rectangles. Rinse and repeat.
- Render the each rectangle as a cube, letting the height value represent the Z.
"""

def MapPlans(size, grid_scale):
    """ 
        Create a three dimensional level of size x size x size.
        The key to the contents of each cube is a tuple.
    """
    level = {}
    x = 0
    while x < size:
        y = 0
        while y < size:
            z = 0
            while z < size:
                level[(x, y, z)] = 0
                z += grid_scale
            y += grid_scale
        x += grid_scale
    return level

def foo(level):
    "Find the corners based on the size of the level"
    bounds = math.sqrt(level)
    subdiv = len(level) / 4
    level[(0, 0, 0)] = 4  # bottom left
    level[(bounds, 0, 0)] = 8  # bottom right
    level[(0, bounds, 0)] = 0  # top left
    level[(bounds, bounds, 0)] = 2  # top right

