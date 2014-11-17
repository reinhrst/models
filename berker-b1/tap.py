import bpy
import shared


def build_tap(base=(0, 0, 0)):
    sideplates = shared.add_sideplates(base)
    raisedplate = shared.add_cuboid("raisedplate", (-40.5, -30, 0),
                                    (81, 60, 13), base)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=256,
        radius=37, depth=10, location=list(map(sum, zip(base, (0, 0, 8)))))
    border = bpy.context.object
    border.name = "border"
    border.hide = True

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=256,
        radius=35, depth=20, location=list(map(sum, zip(base, (0, 0, 5)))))
    cutout = bpy.context.object
    cutout.name = "cutout"
    cutout.hide = True

    shared.boolean_modifier(raisedplate, border, "UNION")
    for item in sideplates + [raisedplate]:
        shared.boolean_modifier(item, cutout, "DIFFERENCE")

    spheremask, spheremask2 = shared.add_spheres(base)

    shared.boolean_modifier(raisedplate, spheremask, "INTERSECT")

    lowercutout = shared.add_cuboid("lowercutout", (-38.5, -28, -10),
                                    (77, 56, 20), base)
    shared.boolean_modifier(lowercutout, spheremask2, "INTERSECT")
    shared.boolean_modifier(lowercutout, border, "DIFFERENCE")
    lowercutout.hide = True

    shared.boolean_modifier(raisedplate, lowercutout, "DIFFERENCE")

    objects = sideplates + [raisedplate]
    shared.select(objects)
    return objects
