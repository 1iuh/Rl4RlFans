from __future__ import annotations

from components.base_component import BaseComponent
import exceptions

from typing import TYPE_CHECKING
from render_order import RenderOrder
import color
from entities.factors import gears
import random
import env_val

if TYPE_CHECKING:
    from entities.entity import Actor


class Fighter(BaseComponent):

    parent: Actor  # type: ignore
    _max_hp: int
    _hp: int
    _defense: int
    _magic: int
    _power: int
    _speed: int
    _max_mp: int
    _mp: int

    def __init__(self, hp: int, defense: int, power: int,
                 speed: int, magic: int):
        self._max_hp = hp
        self._hp = hp
        self._defense = defense
        self._power = power
        self._speed = speed
        self._magic = magic
        self._max_mp = 20
        self._mp = 20

    @property
    def max_hp(self) -> int:
        return self._max_hp + self.parent.equipment.get_stat('max_hp')

    @property
    def defense(self) -> int:
        return self._defense + self.parent.equipment.get_stat('defense')

    @property
    def power(self) -> int:
        return self._power + self.parent.equipment.get_stat('power')

    @property
    def speed(self) -> int:
        return self._speed + self.parent.equipment.get_stat('speed')

    @property
    def magic(self) -> int:
        return self._magic + self.parent.equipment.get_stat('magic')

    @property
    def max_mp(self) -> int:
        return self._max_mp + self.parent.equipment.get_stat('max_mp')

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def mp(self) -> int:
        return self._mp

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @mp.setter
    def mp(self, value):
        self._mp = max(0, min(value, self.max_mp))

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))

        if self._hp == 0 and self.parent.entity_id == 0:
            raise exceptions.PlayerDie
        if self._hp == 0 and self.parent.ai:
            self.die()

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        amount = int(self.max_hp * amount / 100)
        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self._hp = new_hp_value

        return amount_recovered

    def mana_recover(self, amount: int) -> int:
        if self.mp == self.max_mp:
            return 0
        amount = int(self.max_mp * amount / 100)
        new_mp_value = self.mp + amount
        if new_mp_value > self.max_mp:
            new_mp_value = self.max_mp
        amount_recovered = new_mp_value - self.mp
        self._mp = new_mp_value
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self) -> None:
        death_message = f"{self.parent.name} died!"
        death_message_color = color.enemy_die
        self.parent.blocks_movement = False
        self.parent.sprite.is_alive = False
        self.parent.ai = None
        self.parent.name = f"{self.parent.name}'s remain."
        self.parent.sprite.render_order = RenderOrder.CORPSE
        self.engine.message_log.add_message(death_message, death_message_color)
        self.drop_loots()

    def drop_loots(self):
        if not self.parent.is_monster():
            return
        ranval = random.random()
        if ranval < env_val.monster_drop_rate:
            gear = random.choice(gears.all_gears)
            gear.level = self.parent.level
            item = gear.copy()
            item.x = self.parent.x
            item.y = self.parent.y
            self.engine.game_map.spawn_entity(item)

    def to_dict(self):
        return dict(
            max_hp=self._max_hp,
            hp=self._hp,
            defense=self._defense,
            power=self._power,
            speed=self._speed,
            magic=self._magic,
            max_mp=self._max_mp,
            mp=self._mp,
        )

    def load_dict(self, d):
        self._max_hp = d['max_hp']
        self._hp = d['hp']
        self._defense = d['defense']
        self._power = d['power']
        self._speed = d['speed']
        self._magic = d['magic']
        self._max_mp = d['max_mp']
        self._mp = d['mp']
