import bpy, bmesh

# find the grid scale setting
grid_scales = [area.spaces[0].grid_scale for area in bpy.context.screen.areas if area.type == 'VIEW_3D']
scale = grid_scales[0]

bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.data.objects[0].name = "ALM"
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.subdivide()

grid = bmesh.from_edit_mesh(bpy.context.active_object)
mid_vert = int(len(grid.verts) - 1 / 2)
grid.verts[mid_vert].co.z += scale

# create a new mesh from the bmesh, labeled "Mesh"
plane = bpy.data.meshes.new("Mesh")
grid.to_mesh(plane)
grid.free()  # garbage collection?

scene = bpy.context.scene  # the current scene
obj = bpy.data.objects.new("Height Map", plane)  # a new container named Object, filled with our mesh

# add Object to the scene
scene.objects.link(obj)

# grid = bpy.context.active_object.data.vertices
# grid = [i for i in grid]

# mid_vert = int((len(grid) - 1) / 2)
# mid_vert = grid[mid_vert]

# bpy.ops.object.editmode_toggle()
