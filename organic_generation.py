import bpy
import pprint, math, random, time

def MapPlans(size, grid_scale):
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

def CAM(level, scale, smoothing=2):
    """
        Input : 
            level -- Dictionary of vector, int
            scale -- grid scale
            smoothing -- number of iterations
        Returns: Modifies Input Dictionary
    """
    tile_count = 0
    wall_count = 0
    for tile in level:
        # generate a random number
        chance = random.randint(0, 100)
        if chance < 30:  # 30% chance to be a wall
            level[tile] = 1
            wall_count += 1
        tile_count += 1

    print("{}/{}".format(wall_count, tile_count))
    print("Smoothing")
    for i in range(smoothing):
        wall_count += builder(level, scale)
        print("{}/{}".format(wall_count, tile_count))

def builder(level, scale):
    # now check neighbors to see if an empty spot needs to be changed to a wall
    wall_count = 0
    for tile in level:
        if level[tile] == 0:
            # are 4 / 8 of it's neighbors a wall? then make it a wall
            x, y, z = tile
            if fill_check(level, x, y, z, scale, 5):
                level[tile] = 1
                wall_count += 1

        elif level[tile] == 1:
            x, y, z = tile
            if not fill_check(level, x, y, z, scale, 4):
                level[tile] = 0
                wall_count -= 1
    return wall_count

def fill_check(level, x, y, z, scale, threshhold):
    """
        Input: level -- Dictionary of vector, int
                x -- int
                y -- int
                z -- int
                scale -- int
        Returns: Modifies value of level[(x, y, z)]
    """
    # assuming (x, y, z) is in level, check if neighbors are in level
    # if neighbor is in level, check if it is a wall
    # if it is a wall, add to wall count
    # if wall count >= 5, level[(x, y, z)] gets changed to a wall too
    walls = 0

    cursor = (x - scale, y - scale, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x, y + scale, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x + scale, y + scale, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x + scale, y, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x + scale, y - scale, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x, y - scale, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x - scale, y - scale, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    cursor = (x - scale, y, z)
    if cursor in level:
        if level[cursor] == 1:
            walls += 1

    if walls >= threshhold:
        return True

def generate_level(level, scale):
    # for tile in myMap, if tile = 1, make a cube
    # move up one scale
    # for tile in myMap, make a cube
    r = scale / 2
    print("Adding walls and lights!")
    for tile in level:
        if level[tile] == 1:
            bpy.ops.mesh.primitive_cube_add(radius=r, location=tile)
        else:
            if tile[0] % 8 == 0 and tile[1] % 8 == 0 and tile[2] % 8 == 0:
                bpy.ops.object.lamp_add(type='POINT',location=tile)

    # Select everything and move it up a story
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0.0, 0.0, scale))

    print("Adding a floor!")
    for tile in level:
        bpy.ops.mesh.primitive_cube_add(radius=r, location=tile)

    print("Cleanup!")
    active_sanity()
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.join()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.uv.smart_project()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='SELECT')

def active_sanity():
    """ Make a mesh the active object. """
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            bpy.context.scene.objects.active = o
            break

print("\n")
print("Start Time: {}".format(time.strftime("%H:%M:%S")))

grid_scales = [area.spaces[0].grid_scale for area in bpy.context.screen.areas if area.type == 'VIEW_3D']
scale = grid_scales[0]
size = 128
myMap = MapPlans(size, scale)

CAM(myMap, scale, 5)
generate_level(myMap, scale)

print("Adjusting the lights...")
for lamp in bpy.data.lamps:
    if lamp.type == "POINT":
        lamp.energy = .80
        # lamp.distance = scale * .75
        lamp.color = 1.0, 0.754, 0.537

print("End Time: {}".format(time.strftime("%H:%M:%S")))
