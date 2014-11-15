import bpy

bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(0, 0, 0))
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)


# bpy.context.scene.system = "METRIC"
# bpy.context.scene.scale_length = 0.01  # work in cm
# bpy.context.space_data.grid_scale = 0.01

def add_object(name, vertices, faces):
    mesh = bpy.data.meshes.new(name + "_mesh")
    blender_object = bpy.data.objects.new(name + "_ob", mesh)
    bpy.context.scene.objects.link(blender_object)
    mesh.from_pydata(vertices, [], faces)
    return blender_object


def add_cuboid(name, location, size):
    vertices = [[
        max(location[c], location[c] + size[c]) if i & (1 << c) else
        min(location[c], location[c] + size[c]) for c in range(3)]
        for i in range(8)]

    faces = [[1, 0, 2, 3],
             [2, 0, 4, 6],
             [0, 1, 5, 4],
             [4, 5, 7, 6],
             [1, 3, 7, 5],
             [3, 2, 6, 7]]

    return add_object(name, vertices, faces)

add_cuboid("sideplate0", (-4, -4.5, 0), (8, 1.6, 0.5))
add_cuboid("sideplate1", (-4,  4.5, 0), (8, -1.6, 0.5))


topcutout = add_cuboid("topcutout", (-2.8, -2.8, 0.15), (5.6, 5.6, 1))
topcutout.hide = True

innercutout = add_cuboid("innercutout", (-2.6, -2.6, -1), (5.2, 5.2, 3))
bpy.context.scene.objects.active = innercutout
bpy.ops.object.modifier_add(type="BEVEL")
innercutout.modifiers["Bevel"].segments = 5
innercutout.hide = True

sphere_radius = 16.16/0.8
origin = (0, 0, 1.3 - sphere_radius)
bpy.ops.mesh.primitive_uv_sphere_add(size=sphere_radius, location=origin)
spheremask = bpy.context.object
spheremask.name = "spheremask"
spheremask.hide = True

raisedplate = add_cuboid("raisedplate", (-4.05, -3, 0), (8.1, 6, 1))
bpy.context.scene.objects.active = raisedplate

bpy.ops.object.modifier_add(type="BOOLEAN")
raisedplate.modifiers["Boolean"].operation = "INTERSECT"
raisedplate.modifiers["Boolean"].object = spheremask

bpy.ops.object.modifier_add(type="BOOLEAN")
raisedplate.modifiers["Boolean.001"].operation = "DIFFERENCE"
raisedplate.modifiers["Boolean.001"].object = topcutout

bpy.ops.object.modifier_add(type="BOOLEAN")
raisedplate.modifiers["Boolean.002"].operation = "DIFFERENCE"
raisedplate.modifiers["Boolean.002"].object = innercutout


def unhide():
    topcutout.hide = False
    innercutout.hide = False
    spheremask.hide = False
