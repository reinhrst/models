import bpy
import shared


def add_notches(base):
    notches = [
        shared.add_cuboid("notch0", (-15.5, -27.5, -1.5), (5, 55, 4.5), base),
        shared.add_cuboid("notch1", (15.5, -27.5, -1.5), (-5, 55, 4.5), base),
        shared.add_cuboid("notch2", (-27.5, -15.5, -1.5), (55, 5, 4.5), base),
        shared.add_cuboid("notch3", (-27.5, 15.5, -1.5), (55, -5, 4.5), base),
    ]

    for notch, c, mid in zip(notches, (0, 0, 1, 1), (-13, 13, -13, 13)):
        notch.hide = True
        for i in range(4):
            notch.data.vertices[i].co[c] += \
                (mid + base[c] - notch.data.vertices[i].co[c]) / (5.0 / 3)
    return notches


def add_corner_cutouts(base):
    corners = [
        shared.add_cuboid("corner0", (-28, -28, 1), (9.5, 9.5, 10), base),
        shared.add_cuboid("corner1", (28, -28, 1), (-9.5, 9.5, 10), base),
        shared.add_cuboid("corner2", (28, 28, 1), (-9.5, -9.5, 10), base),
        shared.add_cuboid("corner3", (-28, 28, 1), (9.5, -9.5, 10), base),
    ]
    for corner in corners:
        corner.hide = True
    return corners


def build_single(base=(0, 0, 0)):
    sideplates = shared.add_sideplates(base)

    uppercutout = shared.add_cuboid("uppercutout", (-28, -28, 1.5),
                                    (56, 56, 10), base)
    uppercutout.hide = True

    innercutout = shared.add_cuboid("innercutout", (-26, -26, -10),
                                    (52, 52, 30), base)
    bpy.context.scene.objects.active = innercutout
    bpy.ops.object.modifier_add(type="BEVEL")
    innercutout.modifiers["Bevel"].segments = 5
    innercutout.hide = True

    spheremask, spheremask2 = shared.add_spheres(base)

    top_cutout = shared.add_cuboid("top_cutout", (-38, -28, -1), (7, 56, 10),
                                   base)
    bpy.context.scene.objects.active = top_cutout
    bpy.ops.object.modifier_add(type="BOOLEAN")
    top_cutout.modifiers["Boolean"].operation = "INTERSECT"
    top_cutout.modifiers["Boolean"].object = spheremask2
    top_cutout.hide = True

    bottom_cutout = shared.add_cuboid("bottom_cutout", (38, -28, -1),
                                      (-7, 56, 10), base)
    bpy.context.scene.objects.active = bottom_cutout
    bpy.ops.object.modifier_add(type="BOOLEAN")
    bottom_cutout.modifiers["Boolean"].operation = "INTERSECT"
    bottom_cutout.modifiers["Boolean"].object = spheremask2
    bottom_cutout.hide = True

    notches = add_notches(base)
    corners = add_corner_cutouts(base)

    raisedplate = shared.add_cuboid("raisedplate", (-40.5, -30, 0),
                                    (81, 60, 13), base)
    bpy.context.scene.objects.active = raisedplate

    shared.boolean_modifier(raisedplate, spheremask, "INTERSECT")

    for i, cutout in enumerate([uppercutout, innercutout, top_cutout,
                                bottom_cutout] + notches + corners):
        modifier = raisedplate.modifiers.new("Bool", "BOOLEAN")
        modifier.object = cutout
        modifier.operation = "DIFFERENCE"

    objects = sideplates + [raisedplate]
    shared.select(objects)
    return objects
