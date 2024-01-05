import numpy as np  # type: ignore
import constants

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("tilecode", int),  # Graphics for when this tile is not in FOV.
    ]
)

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
   tilecode=constants.floor_tilecode,
)

wall = new_tile(
   walkable=False,
   transparent=False,
   tilecode=constants.wall_tilecode,
)
