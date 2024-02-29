from __future__ import annotations

import copy
import math

from typing import TYPE_CHECKING, Optional, Tuple, Union
import sprites

import constants

if TYPE_CHECKING:
    from game_map import GameMap
    from components.consumable import Consumable
    from components.inventory import Inventory
    from components.fighter import Fighter
    from arcade import Sprite
    from sprites import ActorSprite, ItemSprite, MissileSprite


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        sprite: Optional[Sprite] = None,
    ):

        self.x = x
        self.y = y
        self.name = name
        self.blocks_movement = blocks_movement
        self.sprite = sprite

        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            self.register()

    def register(self):
        """Spawn a copy of this instance at the given location."""
        self.gamemap.entities.add(self)
        self.gamemap.entity_sprites.append(self.sprite)
        return self

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self, gamemap, x, y):
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        gamemap.entity_sprites.append(clone.sprite)
        return clone

    def despawn(self, gamemap: GameMap):
        """Spawn a copy of this instance at the given location."""
        gamemap.entities.remove(self)
        gamemap.entity_sprites.remove(self.sprite)

    def place(self, x, y, gamemap):
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x)**2 + (y - self.y)**2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle baz
        return state

    def to_dict(self):
        return {}


class Actor(Entity):

    sprite: ActorSprite

    def __init__(self,
                 *,
                 x: int = 0,
                 y: int = 0,
                 name: str = "<Unnamed>",
                 sprite: ActorSprite,
                 ai_cls,
                 fighter: Fighter,
                 inventory: Inventory):
        super().__init__(
            x=x,
            y=y,
            name=name,
            blocks_movement=True,
            sprite=sprite,
        )

        self.ai = ai_cls(self)
        self.fighter = fighter
        self.fighter.parent = self
        self.inventory = inventory
        self.inventory.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


class Item(Entity):

    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        sprite: Optional[ItemSprite] = None,
        consumable: Consumable,
    ):
        super().__init__(
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite=sprite,
        )

        self.consumable = consumable
        self.consumable.parent = self


class VisualEffects(Entity):

    sprite: MissileSprite

    def __init__(
        self,
        parent: GameMap,
        sprite: MissileSprite,
        x: int = 0,
        y: int = 0,
        name: str = "Missile",
    ):
        super().__init__(
            parent=parent,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite=sprite,
        )
        self.sprite.set_duration()

    def register(self):
        self.gamemap.missiles.append(self)
        self.sprite.center_x = self.x * constants.grid_size
        self.sprite.center_y = self.y * constants.grid_size
        self.gamemap.missile_sprites.append(self.sprite)
        return self

    def on_update(self):
        if (self.sprite.left_time < 0):
            self.despawn()

    def despawn(self):  # type: ignore
        """Spawn a copy of this instance at the given location."""
        self.gamemap.missiles.remove(self)
        self.gamemap.missile_sprites.remove(self.sprite)
        self.on_despawn()

    def on_despawn(self) -> None:
        pass


class Missile(Entity):

    sprite: MissileSprite
    target_xy: Tuple[int, int]
    radius: int
    damage: int

    def __init__(
        self,
        parent: GameMap,
        target_xy: Tuple[int, int],
        sprite: MissileSprite,
        radius: int,
        damage: int,
        x: int = 0,
        y: int = 0,
        name: str = "Missile",
    ):
        super().__init__(
            parent=parent,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite=sprite,
        )

        self.target_xy = target_xy
        self.radius = radius
        self.damage = damage
        self.sprite.set_target(
            target_x=target_xy[0] * constants.grid_size,
            target_y=target_xy[1] * constants.grid_size,
        )

    def register(self):
        """Spawn a copy of this instance at the given location."""
        self.gamemap.missiles.append(self)
        self.sprite.center_x = self.x * constants.grid_size
        self.sprite.center_y = self.y * constants.grid_size
        self.gamemap.missile_sprites.append(self.sprite)
        return self

    def on_update(self):
        if (self.sprite.left_time < 0):
            self.despawn()

    def despawn(self):  # type: ignore
        """Spawn a copy of this instance at the given location."""
        self.gamemap.missiles.remove(self)
        self.gamemap.missile_sprites.remove(self.sprite)
        self.on_despawn()

    def on_despawn(self) -> None:
        for actor in self.gamemap.actors:
            if actor.distance(*self.target_xy) <= self.radius:
                self.gamemap.engine.message_log.add_message(
                    f"{actor.name} 被炽热的爆炸吞噬, 受到了 {self.damage} 伤害!")
                actor.fighter.take_damage(self.damage)

                VisualEffects(
                    parent=self.gamemap,
                    x=actor.x,
                    y=actor.y,
                    sprite=sprites.flame_sprite(),
                )
