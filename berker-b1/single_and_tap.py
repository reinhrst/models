import single
import tap
import shared


def build(base=(0, 0, 0)):
    tap_items = tap.build_tap((0, -35.5, 0))
    single_items = single.build_single((0, 35.5, 0))
    endplates = shared.add_endplates(base, 2)
    shared.select(tap_items + single_items + endplates)
