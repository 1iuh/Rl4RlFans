from typing import Tuple
import tilesets

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", tilesets.void),  # 3 unsigned bytes, for RGB colors.
        ("bg", tilesets.void),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), 0, 1), dtype=graphic_dt)


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
   dark=tilesets.floor,
   light=tilesets.floor,
)
wall = new_tile(
   walkable=False,
   transparent=False,
   dark=tilesets.wall,
   light=tilesets.wall,
)
