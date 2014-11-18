import shared


def build_tap(base=(0, 0, 0)):
    sideplates = shared.add_sideplates(base)
    raisedplate = shared.add_cuboid("raisedplate", (-40.5, -30, 0),
                                    (81, 60, 13), base)
    border = shared.add_cylincer(
        "border", radius=39, depth=20,
        location=list(map(sum, zip(base, (0, 0, 10)))))
    top_cutout = shared.add_cylincer(
        "top_cutcout", radius=35, depth=20,
        location=list(map(sum, zip(base, (0, 0, 8)))))
    bottom_cutout = shared.add_cylincer(
        "bottom_cutout", radius=38, depth=10,
        location=list(map(sum, zip(base, (0, 0, 0)))))

    shared.boolean_modifier(raisedplate, border, "UNION")
    for item in sideplates + [raisedplate]:
        shared.boolean_modifier(item, top_cutout, "DIFFERENCE")
        shared.boolean_modifier(item, bottom_cutout, "DIFFERENCE")

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
    return (objects, [top_cutout, bottom_cutout])
