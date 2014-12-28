import shared

THICKNESS = 3
WIDTH = 50 + 2 * THICKNESS
LENGTH = 50 + 2 * THICKNESS
HEIGHT = 12 + THICKNESS


def build_box(base=(0, 0, 0)):
    box = shared.add_cuboid("box", (0, 0, 0), (WIDTH, LENGTH, HEIGHT), base)
    cutout = shared.add_cuboid("cutout", (THICKNESS, THICKNESS, THICKNESS + 5),
                               (WIDTH - 2 * THICKNESS, LENGTH - 2 * THICKNESS,
                                HEIGHT), base)
    shared.boolean_modifier(box, cutout, "DIFFERENCE")

    powerco = shared.add_cuboid("powerco", (THICKNESS, -1, 6 + THICKNESS),
                                (8, THICKNESS + 2, HEIGHT), base)
    shared.boolean_modifier(box, powerco, "DIFFERENCE")

    usbco = shared.add_cuboid("usb", (-1, THICKNESS + 3, 7 + THICKNESS),
                              (THICKNESS + 2, 22, HEIGHT), base)
    shared.boolean_modifier(box, usbco, "DIFFERENCE")

    rail1 = shared.add_cuboid("rail1", (THICKNESS, THICKNESS, THICKNESS),
                              (35, 10, HEIGHT), base)
    rail2 = shared.add_cuboid("rail2", (THICKNESS, THICKNESS + 20, THICKNESS),
                              (35, 20, HEIGHT), base)
    shared.boolean_modifier(box, rail1, "DIFFERENCE")
    shared.boolean_modifier(box, rail2, "DIFFERENCE")
    shared.select([box])
    return
