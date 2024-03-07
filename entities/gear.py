from __future__ import annotations

from entities.entity import Entity
from entities.gear_enchantment_data import rate_of_enchant, enchant_stat_value
from random import random, choice
import constants


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
    enchantments = None
    desc: str

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
        self.desc = ''
        self.base_name = name
        self.part = part
        self.consumable = consumable
        self.consumable.parent = self
        self.stats = stats

    def get_stats(self, key):
        base = getattr(self, key)
        extra = getattr(self.enchantments, key)
        return base + extra

    def copy(self):
        clone = super().copy()
        clone.rand()
        return clone

    def rand(self):
        for attr, value in self.stats[self.level].items():
            setattr(self, attr, value)
            if len(self.desc) > 0:
                self.desc = ','.join([self.desc, f"{attr}+{value}"])
            else:
                self.desc = f"{attr}+{value}"
        self.enchantments = GearEnchantment(self.level)
        self.name = (f'+{self.level} {self.enchantments.title} '
                     + self.base_name)

    @property
    def attributes(self):
        if len(self.enchantments.desc) > 0:
            return self.desc + '\n        └ ' + self.enchantments.desc
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

    def put_down(self):
        self.parent.put_down(self)

    def put_on(self):
        self.parent.put_on(self)


class GearParts:
    BODY = 0
    FOOT = 1
    HANDS = 2


class GearEnchantment:
    level = 1
    power = 0
    max_hp = 0
    magic = 0
    defense = 0
    max_mp = 0
    speed = 0
    title: str
    desc: str

    def __init__(self, level):
        self.level = level
        self.desc = ''
        self.title = ''
        rate = rate_of_enchant[self.level]
        ran_val = random()
        count = 0

        if ran_val < rate[1]:
            count = 1
        if ran_val < rate[2]:
            count = 2
        if ran_val < rate[3]:
            count = 3
        self.set_title(count)
        for _ in range(count):
            stat_key = choice(constants.actor_stats_keys)
            val = enchant_stat_value[stat_key][self.level]
            old_val = getattr(self, stat_key)
            setattr(self, stat_key, old_val + val)
            if len(self.desc) > 0:
                self.desc = ','.join([self.desc, f"{stat_key}+{val}"])
            else:
                self.desc = f"{stat_key}+{val}"

    def set_title(self, count):
        if count == 0:
            self.title = "Normal "
        elif count == 1:
            self.title = "Magic  "
        elif count == 2:
            self.title = "Super  "
        elif count == 3:
            self.title = "Amazing"
