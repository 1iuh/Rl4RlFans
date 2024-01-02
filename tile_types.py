from typing import Tuple
import tilesets

import numpy as np  # type: ignore

void = 1000
dark_wall = 1001
light_wall = 1002
dark_floor = 1003
light_floor = 1004

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", int),  # Graphics for when this tile is not in FOV.
        ("light", int),  # Graphics for when the tile is in FOV.
    ]
)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((void), dtype=int)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable,
    transparent,
    dark,
    light
):
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


floor = new_tile(
   walkable=True,
   transparent=True,
   dark=dark_floor,
   light=light_floor,
)
wall = new_tile(
   walkable=False,
   transparent=False,
   dark=dark_wall,
   light=light_wall,
)
