from typing import Tuple
import tilesets

import numpy as np  # type: ignore

wall_tilecode = 1001
floor_tilecode = 1002
void = 1000

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("tilecode", int),  # Graphics for when this tile is not in FOV.
    ]
)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((void), dtype=int)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable,
    transparent,
    tilecode
):
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, tilecode), dtype=tile_dt)


floor = new_tile(
   walkable=True,
   transparent=True,
   tilecode=floor_tilecode,
)
wall = new_tile(
   walkable=False,
   transparent=False,
   tilecode=wall_tilecode,
)
