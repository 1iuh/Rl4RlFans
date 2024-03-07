import numpy as np
import tcod
import random
from engine import GameEngine
from arcade import SpriteList, Sprite

from entities import entity_dict
from entities.factors import actors, gears
from entities.entity import Item
from entities.gear import Gear
from entities.actor import Actor
import tile_types
import sprites
import constants
import pickle
from base64 import b64decode, b64encode

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


class GameMap:
    engine: GameEngine
    level: int

    def __init__(self, engine, width, height, entities, level):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.level = level
        self.tiles = np.full(
            (width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")
        # Tiles the player has seen before
        self.explored = np.full((width, height), fill_value=False, order="F")
        self.construct_sprites = SpriteList()
        self.entity_sprites = SpriteList()

    def spawn_entity(self, entity):
        entity.parent = self
        entity.sprite = entity.sprite_f()
        self.entities.add(entity)
        self.entity_sprites.append(entity.sprite)
        entity.on_spawn()

    def despawn_entity(self, entity):
        self.entities.remove(entity)
        self.entity_sprites.remove(entity.sprite)

    @property
    def visible_monsters(self):
        mobs = []
        for e in self.entities:
            if isinstance(e, Actor) and e.entity_id != 0 and e.sprite.visible:
                mobs.append(e)
        return mobs

    def init_construct_sprites(self):
        x = 0
        y = 0
        self.gamemap.construct_sprites.clear()
        for row in self.gamemap.tiles:
            for col in row:
                cons: Sprite
                if col[2] == constants.floor_tilecode:
                    cons = sprites.floor_sprite()
                elif col[2] == constants.wall_tilecode:
                    cons = sprites.wall_sprite()
                elif col[2] == constants.down_stair_tilecode:
                    cons = sprites.down_stair_sprite()
                else:
                    continue
                cons.center_x = x * constants.grid_size
                cons.center_y = y * constants.grid_size
                self.gamemap.construct_sprites.append(cons)
                y += 1
            y = 0
            x += 1

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
    def items(self):
        yield from (
            entity for entity in self.entities if isinstance(entity,
                                                             (Item, Gear)))

    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at_location(self, location_x, location_y):
        for entity in self.entities:
            if (entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def render(self):
        i = 0
        for row in self.visible:
            for col in row:
                if col:
                    self.construct_sprites[i].set_is_light(True)
                else:
                    self.construct_sprites[i].set_is_light(False)
                i += 1
        i = 0
        for row in self.explored:
            for col in row:
                if col:
                    self.construct_sprites[i].set_is_seen(True)
                i += 1

        self.entity_sprites.sort(key=lambda x: x.render_order.value)

        for entity in self.entities:
            # Only print entities that are in the FOV
            entity.sprite.visible = self.visible[entity.x, entity.y]
            entity.sprite.center_x = entity.x * constants.grid_size
            entity.sprite.center_y = entity.y * constants.grid_size
            # draw hp bar

        self.construct_sprites.draw()
        self.entity_sprites.draw()

    def to_dict(self):
        return dict(
            tiles=b64encode(pickle.dumps(self.tiles)).decode('ascii'),
            visible=b64encode(pickle.dumps(self.visible)).decode('ascii'),
            explored=b64encode(pickle.dumps(self.explored)).decode('ascii'),
            entities=[e.to_dict() for e in self.entities]
        )

    def load_dict(self, d):
        self.tiles = pickle.loads(b64decode(d['tiles']))
        self.visible = pickle.loads(b64decode(d['visible']))
        self.explored = pickle.loads(b64decode(d['explored']))
        self.init_construct_sprites()
        self.entities.clear()
        self.entity_sprites.clear()
        for entity_data in d['entities']:
            if entity_data['entity_id'] == 0:
                continue
            entity: Entity = entity_dict[entity_data['entity_id']].copy()
            self.spawn_entity(entity)
            entity.load_dict(entity_data)


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


def place_entities(room, dungeon, maximum_monsters, maximum_items, level):
    number_of_monsters = random.randint(0, maximum_monsters)
    number_of_items = random.randint(0, maximum_items)

    for _ in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        val = random.random()
        if val > 0.8:
            continue

        if not any(entity.x == x and entity.y == y
                   for entity in dungeon.entities):
            actors.a_tree.level = level
            entity = actors.a_tree.copy()
            entity.x = x
            entity.y = y
            dungeon.spawn_entity(entity)

    for _ in range(number_of_items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y
                   for entity in dungeon.entities):
            item_chance = random.random()

            if item_chance < 0.1:
                gears.boots.level = level
                item = gears.boots.copy()
                item.x = x
                item.y = y
                dungeon.spawn_entity(item)
            elif item_chance < 0.2:
                gears.plate_mail.level = level
                item = gears.plate_mail.copy()
                item.x = x
                item.y = y
                dungeon.spawn_entity(item)
            elif item_chance < 0.3:
                gears.wand.level = level
                item = gears.wand.copy()
                item.x = x
                item.y = y
                dungeon.spawn_entity(item)


def generate_dungeon(
        map_width,
        map_height,
        room_min_size,
        room_max_size,
        max_rooms,
        max_monsters_per_room,
        max_items_per_room,
        level,
        engine,
):
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height,
                      entities=[player], level=level)

    rooms = []

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(8, dungeon.width - room_width - 1)
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
            player.x = new_room.center[0]
            player.y = new_room.center[1]
            dungeon.spawn_entity(player)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon, max_monsters_per_room,
                       max_items_per_room, level)

        # Finally, append the new room to the list.
        rooms.append(new_room)

    # put stair
    room = random.choice(rooms)
    dungeon.tiles[room.center] = tile_types.down_stair

    dungeon.init_construct_sprites()
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
