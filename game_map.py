
import numpy as np
import tcod
import random
import entity_factories
from entity import Actor, Item

import tile_types

from typing import Iterator


class GameMap:
    def __init__(self, engine, width, height, entities):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    @property
    def gamemap(self):
        return self

    @property
    def actors(self):
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))


    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at_location(self, location_x, location_y):
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def render(self, console):
        """
        Renders the map.
 
        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )
        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                        x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                   )


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self):
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities( room, dungeon, maximum_monsters, maximum_items):
   number_of_monsters = random.randint(0, maximum_monsters)
   number_of_items = random.randint(0, maximum_items)

   for i in range(number_of_monsters):
       x = random.randint(room.x1 + 1, room.x2 - 1)
       y = random.randint(room.y1 + 1, room.y2 - 1)

       if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
           entity = random.choice(entity_factories.all_entities)
           entity.spawn(dungeon, x, y)
   for i in range(number_of_items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity_factories.health_potion.spawn(dungeon, x, y)

def generate_dungeon(
   map_width,
   map_height,
   room_min_size,
   room_max_size,
   max_rooms,
   max_monsters_per_room,
   max_items_per_room,
   engine,
):
   """Generate a new dungeon map."""
   player = engine.player
   dungeon = GameMap(engine, map_width, map_height, entities=[player])

   rooms = []

   for r in range(max_rooms):
       room_width = random.randint(room_min_size, room_max_size)
       room_height = random.randint(room_min_size, room_max_size)

       x = random.randint(0, dungeon.width - room_width - 1)
       y = random.randint(0, dungeon.height - room_height - 1)

       # "RectangularRoom" class makes rectangles easier to work with
       new_room = RectangularRoom(x, y, room_width, room_height)

       # Run through the other rooms and see if they intersect with this one.
       if any(new_room.intersects(other_room) for other_room in rooms):
           continue  # This room intersects, so go to the next attempt.
       # If there are no intersections then the room is valid.

       # Dig out this rooms inner area.
       dungeon.tiles[new_room.inner] = tile_types.floor

       if len(rooms) == 0:
           # The first room, where the player starts.
           player.place(*new_room.center, dungeon)
       else:  # All rooms after the first.
           # Dig out a tunnel between this room and the previous one.
           for x, y in tunnel_between(rooms[-1].center, new_room.center):
               dungeon.tiles[x, y] = tile_types.floor


       place_entities(new_room, dungeon, max_monsters_per_room, max_items_per_room)

       # Finally, append the new room to the list.
       rooms.append(new_room)

   return dungeon


def tunnel_between(start, end):
   """Return an L-shaped tunnel between these two points."""
   x1, y1 = start
   x2, y2 = end
   if random.random() < 0.5:  # 50% chance.
       # Move horizontally, then vertically.
       corner_x, corner_y = x2, y1
   else:
       # Move vertically, then horizontally.
       corner_x, corner_y = x1, y2

   # Generate the coordinates for this tunnel.
   for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
       yield x, y
   for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
       yield x, y
