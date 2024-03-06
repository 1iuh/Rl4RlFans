from __future__ import annotations

from entities.entity import Entity


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.consumable import Consumable


class Gear(Entity):
    level = 1
    power = 0
    max_hp = 0
    magic = 0
    defense = 0
    max_mp = 0
    speed = 0

    def __init__(
        self,
        *,
        consumable: Consumable,
        entity_id: int = 0,
        part: int = 0,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        stats: dict,
        sprite_f=None,
    ):
        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite_f=sprite_f,
        )
        self.part = part
        self.consumable = consumable
        self.consumable.parent = self
        self.stats = stats

    def on_spawn(self):
        self.name = self.name + f' +{self.level}'
        for attr, value in self.stats[self.level].items():
            setattr(self, attr, value)

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
        )

    def load_dict(self, d):
        self.x = d['x']
        self.y = d['y']

    def put_down(self):
        self.parent.put_down(self)

    def put_on(self):
        self.parent.put_on(self)


class GearParts:
    BODY = 0
    FOOT = 1
    HANDS = 2
