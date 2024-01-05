from __future__ import annotations

import copy
import math

from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from game_map import GameMap
    from components.consumable import Consumable
    from components.inventory import Inventory
    from arcade import Sprite
    from sprites import ActorSprite, ItemSprite


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
        self.hasAnimation = False
        self.sprite = sprite

        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

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
        return clone

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
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Actor(Entity):

    sprite: ActorSprite

    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        sprite: ActorSprite,
        ai_cls,
        fighter,
        inventory
    ):
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
