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
