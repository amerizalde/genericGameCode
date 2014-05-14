import bpy, bmesh, pprint

vertLookup = {}
for o in bpy.context.scene.objects:
    try:
        vertLookup[o] = o.data.vertices.values()
    except:
        print("\nNot a mesh: {}".format(o))
     
objects = [o for o in bpy.context.scene.objects]
pprint.pprint(vertLookup)
for o in objects:
    if o in vertLookup:
        vertLookup[o] = [vertLookup[o][i].co for i in range(len(vertLookup[o]))]

print("\n")
pprint.pprint(vertLookup)

def active_sanity():
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            bpy.context.scene.objects.active = o
            break
active_sanity()
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.remove_doubles()
