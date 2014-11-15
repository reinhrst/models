import bpy


def cleanup():
    bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(0, 0, 0))
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete(use_global=False)

    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)


def setup():
    # seems to not work
    return
    bpy.context.scene.system = "METRIC"
    bpy.context.scene.scale_length = 0.01  # work in cm
    bpy.context.space_data.grid_scale = 0.01


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


def add_notches():
    notches = []
    notch0 = add_cuboid("notch0", (-1.55, -2.75, -0.15), (0.5, 5.5, 0.45))
    for i in range(4):
        notch0.data.vertices[i].co[0] += \
            (-1.3 - notch0.data.vertices[i].co[0]) / (0.5 / 0.3)

    notch0.select = True
    notch0.hide = True
    notches.append(notch0)
    bpy.ops.object.duplicate()
    bpy.context.selected_objects[0].name = "notch1_ob"
    for notch in bpy.context.selected_objects:
        for vertix in notch.data.vertices:
            vertix.co[0] += 2.6
        notches.append(notch)

    notch0.select = True
    notch0.select = True
    bpy.ops.object.duplicate()
    bpy.context.selected_objects[0].name = "notch2_ob"
    bpy.context.selected_objects[1].name = "notch3_ob"

    for notch in bpy.context.selected_objects:
        for vertix in notch.data.vertices:
            vertix.co[0], vertix.co[1] = \
                -vertix.co[1], vertix.co[0]
        notches.append(notch)
    return notches


def add_corner_cutouts():
    corners = [
        add_cuboid("corner0", (-2.8, -2.8, 0.1), (0.95, 0.95, 1)),
        add_cuboid("corner1", (2.8, -2.8, 0.1), (-0.95, 0.95, 1)),
        add_cuboid("corner2", (2.8, 2.8, 0.1), (-0.95, -0.95, 1)),
        add_cuboid("corner3", (-2.8, 2.8, 0.1), (0.95, -0.95, 1)),
    ]
    for corner in corners:
        corner.hide = True
    return corners


def build_single(base=(0, 0, 0)):
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

    bpy.ops.object.modifier_add(type="SUBSURF")
    spheremask.modifiers["Subsurf"].levels = 3

    spheremask.hide = True
    spheremask.select = False

    notches = add_notches()
    corners = add_corner_cutouts()

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

    for i, notch in enumerate(notches):
        bpy.ops.object.modifier_add(type="BOOLEAN")
        raisedplate.modifiers["Boolean.%03d" % (i+3)].operation = "DIFFERENCE"
        raisedplate.modifiers["Boolean.%03d" % (i+3)].object = notch

    for i, corner in enumerate(corners):
        bpy.ops.object.modifier_add(type="BOOLEAN")
        raisedplate.modifiers["Boolean.%03d" % (i+7)].operation = "DIFFERENCE"
        raisedplate.modifiers["Boolean.%03d" % (i+7)].object = corner
