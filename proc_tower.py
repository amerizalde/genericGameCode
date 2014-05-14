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

def TipsyWalk(level, grid_scale=1, position=(0, 0, 0), stepsToWalk=0, drop=1, count=0):
    """
        Modified Drunkard Walk algorithm.
        Starting at "position", walk around "level" for
        "stepsToWalk", and change tile to == "drop". This
        version does not walk over tiles that are already
         == to "drop".
    """
    bounds = int(math.floor(pow(len(level), float(1/3))))
    bowl = [0, -grid_scale, grid_scale]
    stepsTaken = 0
    while stepsTaken < stepsToWalk:
        # 1 - make three choices.
        x = random.choice(bowl)
        y = random.choice(bowl)
        position = (position[0] + x, position[1] + y, 0)
        print ("Moving: {}".format(position))
        # 2a - check if position to move to is valid
        if position in level:
            # 3 - have we already walked here?
            if level[position] != drop:
                # 4a - map starts as filled, mark as empty space
                level[position] = drop
                stepsTaken += 1
                count += 1
            # else:
            #     # 4b - new position was in level, but already walked on, so try again
        # 2b - wasn't valid
        else:
            x = int(random.randrange(0, bounds) * grid_scale)
            y = int(random.randrange(0, bounds) * grid_scale)
            z = 0
            if (x, y, z) in level:
                level[(x, y, z)] = drop
                stepsTaken += 1
                count += 1

    print("Bounds: {}".format(bounds * bowl[2]))
    print("rooms: {}".format(count))

def generate_level(levels, plan, size, scale, steps, drop):
    while levels > 0:
        # don't overwrite the original dictionary!
        lvl = plan.copy()
        # pprint.pprint(lvl)
        TipsyWalk(lvl, grid_scale=scale, position=(0, 0, 0), stepsToWalk=steps, drop=drop)
        # pprint.pprint(lvl)
        # add interior walls
        for i in lvl:
            if lvl[i] == 0:
                # WALLS!
                bpy.ops.mesh.primitive_cube_add(radius=2, location=i)
            else:
                # LIGHTS!
                if i[0] % 8 == 0 and i[1] % 8 == 0 and i[2] % 8 == 0:
                    bpy.ops.object.lamp_add(type='POINT',location=i)

        # Select everything and move it up a story
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0.0, 0.0, scale))

        # add floor
        for i in lvl:
            bpy.ops.mesh.primitive_cube_add(radius=2, location=i)

        # Select everything and move it up a story
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0.0, 0.0, scale))

        print("Level {} Complete".format(levels))
        levels -= 1
    # don't overwrite the original dictionary!
    lvl = plan.copy()
    TipsyWalk(lvl, grid_scale=scale, position=(0, 0, 0), stepsToWalk=steps, drop=drop)

    # add interior walls
    for i in lvl:
        if lvl[i] == 0:
            # WALLS!
            bpy.ops.mesh.primitive_cube_add(radius=2, location=i)
        else:
            # LIGHTS!
            if i[0] % 8 == 0 and i[1] % 8 == 0 and i[2] % 8 == 0:
                bpy.ops.object.lamp_add(type='POINT',location=i)

    # Select everything and move it up a story
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0.0, 0.0, scale))

    # add floor
    for i in lvl:
        bpy.ops.mesh.primitive_cube_add(radius=2, location=i)

    active_sanity()
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.join()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.uv.smart_project()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='SELECT')
    print("Level {} Complete".format(levels))

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
size = 64
myMap = MapPlans(size, scale)
steps = int(len(myMap) * .60)  # walk 60% of the length of known Cube
drop = 1  # the breadcrumbs

generate_level(0, myMap, size, scale, steps, drop)

for lamp in bpy.data.lamps:
    if lamp.type == "POINT":
        lamp.energy = .80
        # lamp.distance = scale * .75
        lamp.color = 1.0, 0.754, 0.537

print("Steps to Walk: {}/{}".format(steps, int(len(myMap))))
print("End Time: {}".format(time.strftime("%H:%M:%S")))
