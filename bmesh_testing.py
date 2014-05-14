import pprint, math, random
import bpy, bmesh, mathutils

def testMesh(map_dict):
    # creates a bmesh, no points
    bm = bmesh.new()
    mat = mathutils.Matrix()
    bmesh.ops.create_grid(bm, 1, 1, 4, mat)
    
rooms = {}
mesh = testMesh(rooms)
scene = bpy.context.scene  # the current scene
obj = bpy.data.objects.new("Object", me)  # a new container named Object, filled with our mesh

# add Object to the scene
scene.objects.link(obj)

# make it the active selection
scene.objects.active = obj
obj.select = True
