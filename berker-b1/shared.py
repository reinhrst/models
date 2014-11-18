import bpy


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


def add_cuboid(name, location, size, base):
    vertices = [
        [
            max(location[c] + base[c], location[c] + base[c] + size[c])
            if i & (1 << c) else
            min(location[c] + base[c], location[c] + base[c] + size[c])
            for c in range(3)]
        for i in range(8)]

    faces = [[1, 0, 2, 3],
             [2, 0, 4, 6],
             [0, 1, 5, 4],
             [4, 5, 7, 6],
             [1, 3, 7, 5],
             [3, 2, 6, 7]]

    return add_object(name, vertices, faces)


def add_endplates(base, nrblocks):
    nrhops = nrblocks - 1
    endplate0 = add_cuboid("endplate0", (-40, -45 - 35.5 * nrhops, 0),
                           (80, 9, 5), base)
    endplate1 = add_cuboid("endplate1", (-40, 45 + 35.5 * nrhops, 0),
                           (80, -9, 5), base)

    boolean_modifier(endplate0, add_cuboid("endplate0_cut",
                                           (-38, -43 - 35.5 * nrhops, -2),
                                           (76, 9, 5), base), "DIFFERENCE")
    boolean_modifier(endplate1, add_cuboid("endplate1_cut",
                                           (-38, 43 + 35.5 * nrhops, -2),
                                           (76, -9, 5), base), "DIFFERENCE")

    return [endplate0, endplate1]


def add_cylincer(name, radius, depth, location):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth,
                                        location=location, vertices=256)
    item = bpy.context.object
    item.name = name
    item.select = False
    return item


def add_sideplates(base):
    sideplate0_co = add_cuboid("sideplate0_cutout", (-38, -43, -2),
                               (76, 16, 5), base)
    sideplate0_co.hide = True
    sideplate0 = add_cuboid("sideplate0", (-40, -36, 0), (80, 7, 5), base)
    bpy.context.scene.objects.active = sideplate0
    bpy.ops.object.modifier_add(type="BOOLEAN")
    sideplate0.modifiers["Boolean"].operation = "DIFFERENCE"
    sideplate0.modifiers["Boolean"].object = sideplate0_co

    sideplate1_co = add_cuboid("sideplate1_cutout", (-38, 43, -2),
                               (76, -16, 5), base)
    sideplate1_co.hide = True
    sideplate1 = add_cuboid("sideplate1", (-40,  36, 0), (80, -7, 5), base)
    bpy.context.scene.objects.active = sideplate1
    bpy.ops.object.modifier_add(type="BOOLEAN")
    sideplate1.modifiers["Boolean"].operation = "DIFFERENCE"
    sideplate1.modifiers["Boolean"].object = sideplate1_co

    return [sideplate0, sideplate1]


def add_spheres(base):
    sphere_radius = 161.6/0.8
    origin = list(map(sum, zip([0, 0, 13 - sphere_radius], base)))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=7,
                                          size=sphere_radius, location=origin)
    spheremask = bpy.context.object
    spheremask.name = "spheremask"

    spheremask.hide = True
    spheremask.select = False

    origin[2] -= 2
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=7,
                                          size=sphere_radius, location=origin)
    spheremask2 = bpy.context.object
    spheremask2.name = "spheremask2"
    spheremask2.hide = True
    spheremask2.select = False
    return (spheremask, spheremask2)


def select(objects):
    """
    makes sure that these and only these items are selected
    """
    deselect_all()
    for item in objects:
        item.select = True


def deselect_all():
    selected_objects_copy = list(bpy.context.selected_objects)
    for item in selected_objects_copy:
        item.select = False


def boolean_modifier(sourceobject, mask, operation):
    modifier = sourceobject.modifiers.new("Bool_" + mask.name, "BOOLEAN")
    modifier.operation = operation
    modifier.object = mask
    mask.hide = True
