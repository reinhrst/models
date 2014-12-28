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


def add_cylincer(name, radius, depth, location):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth,
                                        location=location, vertices=256)
    item = bpy.context.object
    item.name = name
    item.select = False
    return item


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
