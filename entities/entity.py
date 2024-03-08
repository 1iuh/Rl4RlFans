from __future__ import annotations

import math
import sprites
import copy
from components.ai import VfxAI

from typing import TYPE_CHECKING, Optional, Tuple, Union

if TYPE_CHECKING:
    from game_map import GameMap
    from components.consumable import Consumable
    from components.inventory import Inventory
    from sprites import MissileSprite


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]
    entity_id: int

    def __init__(
        self,
        entity_id: int = 0,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        sprite_f=None,
    ):

        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.name = name
        self.blocks_movement = blocks_movement
        self.sprite_f = sprite_f

        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent

    def on_spawn(self):
        pass

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def copy(self):
        """Spawn a copy of this instance at the given location."""
        self.parent = None
        clone = copy.deepcopy(self)
        return clone

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and
        the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x)**2 + (y - self.y)**2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def to_dict(self):
        raise NotImplementedError


class Item(Entity):

    def __init__(
        self,
        *,
        entity_id: int = 0,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        sprite_f=None,
        desc,
        consumable: Consumable,
    ):
        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite_f=sprite_f,
        )

        self.desc = desc
        self.consumable = consumable
        self.consumable.parent = self

    @property
    def attributes(self):
        return self.desc

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
        )

    def load_dict(self, d):
        self.x = d['x']
        self.y = d['y']


class VisualEffects(Entity):

    sprite: MissileSprite

    def __init__(
        self,
        entity_id: int,
        sprite_f,
        ai_cls,
        actor,
        name: str = "Missile",
    ):
        self.entity_id = entity_id
        self.name = name
        self.blocks_movement = False
        self.sprite_f = sprite_f

        self.actor = actor
        self.ai = ai_cls(self)

    @property
    def x(self):
        return self.actor.x

    @property
    def y(self):
        return self.actor.y

    def activate(self):
        self.gamemap.despawn_entity(self)

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
            name=self.name,
        )

    def load_dict(self, d):
        self.x = d['x']
        self.y = d['y']


class Missile(Entity):

    sprite: MissileSprite
    target_xy: Tuple[int, int]
    radius: int
    damage: int

    def __init__(
        self,
        entity_id: int,
        parent: GameMap,
        target_xy: Tuple[int, int],
        sprite_f,
        radius: int,
        damage: int,
        ai_cls,
        x: int = 0,
        y: int = 0,
        name: str = "Missile",
    ):
        super().__init__(
            entity_id=entity_id,
            parent=parent,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite_f=sprite_f,
        )

        self.ai = ai_cls(self)
        self.target_xy = target_xy
        self.radius = radius
        self.damage = damage

    def on_spawn(self):
        self.sprite.set_target(
                self.x,
                self.y,
                self.target_xy[0],
                self.target_xy[1],
        )

    def distance2target(self):
        return self.distance(self.target_xy[0], self.target_xy[1])

    def activate(self):
        self.gamemap.despawn_entity(self)
        vfxs = []
        for actor in self.gamemap.actors:
            if actor.distance(*self.target_xy) <= self.radius:
                self.gamemap.engine.message_log.add_message(
                    f"a fireball explodes, {actor.name} \
                            takes {self.damage} damage!")
                actor.fighter.take_damage(self.damage)
                vfx = VisualEffects(
                    9000,
                    sprite_f=sprites.flame_sprite,
                    ai_cls=VfxAI,
                    actor=actor
                )
                vfxs.append(vfx)
        for v in vfxs:
            self.gamemap.spawn_entity(v)

    def copy(self):
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        return clone

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
            target_xy=self.target_xy,
            damage=self.damage,
            radius=self.radius,
            name=self.name,
        )

    def load_dict(self, d):
        self.x = d['x']
        self.y = d['y']
        self.target_xy = d['target_xy']
        self.damage = d['damage']
        self.radius = d['radius']
        self.name = d['name']
