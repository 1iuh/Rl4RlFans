from __future__ import annotations

from entities.entity import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.consumable import Consumable


class Gear(Entity):

    def __init__(
        self,
        *,
        consumable: Consumable,
        entity_id: int = 0,
        part: int = 0,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        sprite_f=None,
    ):
        self.part = part
        self.consumable = consumable
        self.consumable.parent = self

        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite_f=sprite_f,
        )

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
        )

    def load_dict(self, d):
        self.x = d['x']
        self.y = d['y']

    def wear(self):
        self.parent.wear(self)


class GearParts:
    HELMET = 0
    BODY = 1
    LEG = 2
    FOOT = 3
    LEFT_HAND = 4
    RIGHT_HAND = 5
