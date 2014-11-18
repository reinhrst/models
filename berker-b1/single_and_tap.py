import single
import tap
import shared


def build(base=(0, 0, 0)):
    (tap_items, tap_cutouts) = tap.build_tap((0, -35.5, 0))
    (single_items, single_cutouts) = single.build_single((0, 35.5, 0))
    endplates = shared.add_endplates(base, 2)
    for cutout in tap_cutouts:
        for item in single_items + endplates:
            shared.boolean_modifier(item, cutout, "DIFFERENCE")
    for cutout in single_cutouts:
        for item in tap_items + endplates:
            shared.boolean_modifier(item, cutout, "DIFFERENCE")
    shared.select(tap_items + single_items + endplates)
