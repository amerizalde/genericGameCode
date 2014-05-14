import math, random, pprint, bpy

# Divide the rectangle into 4 subrectangles,
# and let their height values be the mean values
# of the corners of the parent rectangle.

def MapPlans(size, grid_scale=1):
    """ 
        Create a two dimensional level of size x size.
        The key to the contents of each cube is a tuple.
    """
    level = {}
    x = 0
    while x < size:
        y = 0
        while y < size:
            z = 0
            level[(x, y, z)] = 0
            y += grid_scale
        x += grid_scale
    return level

def turtles(grid, bounds, roughness):
    """
        Diamond step for every square in the array.
        Square step for every diamond in the array.
    """
    for i in range(bounds):
        # Diamond step
        for point in grid:
            grid[point] = random.choice(roughness) + diamond_value(grid, point)

        # Square step
        for point in grid:
            grid[point] = random.choice(roughness) + square_value(grid, point)

        # Reduce Roughness by a percent value
        if roughness[0] != roughness[len(roughness) - 1]:
            roughness = [i for i in range(roughness[0] + 1, roughness[len(roughness) - 1])]

def diamond_value(grid, point):
    """
        Find the 'diamond' neighbors of point.
        Return the mean average of those points.
    """
    x, y, z = point
    total = 0
    n = 0
    scale = 1

    cursor = (x, y + scale, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    cursor = (x + scale, y, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    cursor = (x, y - scale, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    cursor = (x - scale, y, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    if n != 0:
        return total / n
    else:
        return 0

def square_value(grid, point):
    """
        Find the 'square' neighbors of point.
        Return the mean average of those points.
    """
    x, y, z = point
    total = 0
    n = 0
    scale = 1

    cursor = (x - scale, y - scale, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    cursor = (x + scale, y + scale, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    cursor = (x + scale, y - scale, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    cursor = (x - scale, y - scale, z)
    if cursor in grid:
        total += grid[cursor]
        n += 1

    if n != 0:
        return total / n
    else:
        return 0

def spiral(X, Y, grid, roughness, intensity):
    '''http://stackoverflow.com/questions/398299/looping-in-a-spiral'''
    x = y = 0
    dx = 0
    dy = -1
    half_X = X/2
    half_Y = Y/2
    total = max(X, Y)**2
    for i in range(total):
        if (-half_X < x <= half_X) and (-half_Y < y <= half_Y):
            # print (x, y)
            # DO STUFF...
            if (x, y, 0) in grid:
                grid[(x, y, 0)] += ((random.random() * roughness) + diamond_value(grid, (x, y, 0))) / intensity
                grid[(x, y, 0)] += ((random.random() * roughness) + square_value(grid, (x, y, 0))) / intensity
            else:
                grid[(x, y, 0)] = 20
            # print("pass: ", i, "of ", total)
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

# Main

# find the grid scale setting
grid_scales = [area.spaces[0].grid_scale for area in bpy.context.screen.areas if area.type == 'VIEW_3D']
scale = grid_scales[0]

# the radius of the cube needs to be half the grid scale to fit 1:1
r = scale / 2

# how big will the final map be?
userInput = 33

# iterations
depth = 16

# generate a initial array
# is actually a dictionary with (x, y, z) coords for keys
initSquare = {}

# # store the max x, y of the array
# BOUNDS = max(i for i in initSquare)
RADIUS = int(math.floor(userInput / 2))

# # To be a user editable value between 0.0 and 1.0
# ROUGHNESS_FACTOR = random.random()
ROUGHNESS = 8

# 1 - 100
INTENSITY = 50

# INITIAL_HEIGHT = r

# assign height values to the 4 corners and mid point of the map
initSquare[(-scale, scale, 0)] = a = userInput
initSquare[(-scale, -scale, 0)] = b = userInput
initSquare[(scale, scale, 0)] = c = userInput
initSquare[(scale, -scale, 0)] = d = userInput
initSquare[(0, 0, 0)] = ROUGHNESS + ((a + b + c + d) / 4)

for i in range(depth):
    # assign height values to the rest of the points on the map
    spiral(userInput, userInput, initSquare, ROUGHNESS, INTENSITY)
    print("pass: ", i, "of ", depth)

# For each point, Blender generates a cube and changes the z scale to the height value.
for point in initSquare:
    bpy.ops.mesh.primitive_cube_add(radius=r, location=point)

    # change origin point
    bpy.context.scene.cursor_location = bpy.context.active_object.location
    bpy.context.scene.cursor_location.z -= r
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

    # Ensure that the z scale does not invert below the radius
    bpy.context.active_object.scale.z += int(initSquare[point])

    # apply the scale changes
    bpy.ops.object.transform_apply(scale=True)

pprint.pprint(initSquare)
