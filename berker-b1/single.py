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
    bpy.context.scene.scale_length = 0.001  # work in mm
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
    notch0 = add_cuboid("notch0", (-15.5, -27.5, -1.5), (5., 55., 4.5))
    for i in range(4):
        notch0.data.vertices[i].co[0] += \
            (-13 - notch0.data.vertices[i].co[0]) / (5 / 3)

    notch0.select = True
    notch0.hide = True
    notches.append(notch0)
    bpy.ops.object.duplicate()
    bpy.context.selected_objects[0].name = "notch1_ob"
    for notch in bpy.context.selected_objects:
        for vertix in notch.data.vertices:
            vertix.co[0] += 26
        notches.append(notch)

    notch0.select = True
    bpy.ops.object.duplicate()
    bpy.context.selected_objects[0].name = "notch2_ob"
    bpy.context.selected_objects[1].name = "notch3_ob"

    for notch in bpy.context.selected_objects:
        for vertix in notch.data.vertices:
            vertix.co[0], vertix.co[1] = \
                -vertix.co[1], vertix.co[0]
        notches.append(notch)
        notch.select = False
    return notches


def add_corner_cutouts():
    corners = [
        add_cuboid("corner0", (-28, -28, 1), (9.5, 9.5, 10)),
        add_cuboid("corner1", (28, -28, 1), (-9.5, 9.5, 10)),
        add_cuboid("corner2", (28, 28, 1), (-9.5, -9.5, 10)),
        add_cuboid("corner3", (-28, 28, 1), (9.5, -9.5, 10)),
    ]
    for corner in corners:
        corner.hide = True
    return corners


def build_single(base=(0, 0, 0)):
    sideplate0_co = add_cuboid("sideplate0_cutout", (-38, -43, -2),
                               (76, 16, 5))
    sideplate0_co.hide = True
    sideplate0 = add_cuboid("sideplate0", (-40, -45, 0), (80, 16, 5))
    bpy.context.scene.objects.active = sideplate0
    bpy.ops.object.modifier_add(type="BOOLEAN")
    sideplate0.modifiers["Boolean"].operation = "DIFFERENCE"
    sideplate0.modifiers["Boolean"].object = sideplate0_co

    sideplate1_co = add_cuboid("sideplate1_cutout", (-38, 43, -2),
                               (76, -16, 5))
    sideplate1_co.hide = True
    sideplate1 = add_cuboid("sideplate1", (-40,  45, 0), (80, -16, 5))
    bpy.context.scene.objects.active = sideplate1
    bpy.ops.object.modifier_add(type="BOOLEAN")
    sideplate1.modifiers["Boolean"].operation = "DIFFERENCE"
    sideplate1.modifiers["Boolean"].object = sideplate1_co

    uppercutout = add_cuboid("uppercutout", (-28, -28, 1.5), (56, 56, 10))
    uppercutout.hide = True

    innercutout = add_cuboid("innercutout", (-26, -26, -10), (52, 52, 30))
    bpy.context.scene.objects.active = innercutout
    bpy.ops.object.modifier_add(type="BEVEL")
    innercutout.modifiers["Bevel"].segments = 5
    innercutout.hide = True

    sphere_radius = 161.6/0.8
    origin = [0, 0, 13 - sphere_radius]
    bpy.ops.mesh.primitive_uv_sphere_add(size=sphere_radius, location=origin)
    spheremask = bpy.context.object
    spheremask.name = "spheremask"

    bpy.ops.object.modifier_add(type="SUBSURF")
    spheremask.modifiers["Subsurf"].levels = 3

    spheremask.hide = True
    spheremask.select = False

    origin[2] -= 2
    bpy.ops.mesh.primitive_uv_sphere_add(size=sphere_radius, location=origin)
    spheremask2 = bpy.context.object
    spheremask2.name = "spheremask2"
    bpy.ops.object.modifier_add(type="SUBSURF")
    spheremask2.modifiers["Subsurf"].levels = 1
    spheremask2.hide = True
    spheremask2.select = False

    top_cutout = add_cuboid("top_cutout", (-38, -28, -1), (6, 56, 10))
    bpy.context.scene.objects.active = top_cutout
    bpy.ops.object.modifier_add(type="BOOLEAN")
    top_cutout.modifiers["Boolean"].operation = "INTERSECT"
    top_cutout.modifiers["Boolean"].object = spheremask2
    top_cutout.hide = True

    bottom_cutout = add_cuboid("bottom_cutout", (38, -28, -1), (-6, 56, 10))
    bpy.context.scene.objects.active = bottom_cutout
    bpy.ops.object.modifier_add(type="BOOLEAN")
    bottom_cutout.modifiers["Boolean"].operation = "INTERSECT"
    bottom_cutout.modifiers["Boolean"].object = spheremask2
    bottom_cutout.hide = True

    notches = add_notches()
    corners = add_corner_cutouts()

    raisedplate = add_cuboid("raisedplate", (-40.5, -30, 0), (81, 60, 10))
    bpy.context.scene.objects.active = raisedplate

    bpy.ops.object.modifier_add(type="BOOLEAN")
    raisedplate.modifiers["Boolean"].operation = "INTERSECT"
    raisedplate.modifiers["Boolean"].object = spheremask

    for i, cutout in enumerate([uppercutout, innercutout, top_cutout,
                                bottom_cutout] + notches + corners):
        bpy.ops.object.modifier_add(type="BOOLEAN")
        raisedplate.modifiers["Boolean.%03d" % (i+1)].operation = "DIFFERENCE"
        raisedplate.modifiers["Boolean.%03d" % (i+1)].object = cutout

    sideplate0.select = True
    sideplate1.select = True
    raisedplate.select = True
