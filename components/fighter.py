from __future__ import annotations

from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler

from typing import TYPE_CHECKING
from render_order import RenderOrder
import color

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
                 speed: int):
        self._max_hp = hp
        self._hp = hp
        self._defense = defense
        self._power = power
        self._speed = speed
        self._magic = 0
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

        if self._hp == 0 and self.parent.ai:
            self.die()

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You die."
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent.name} 被杀死了!"
            death_message_color = color.enemy_die

        self.parent.blocks_movement = False
        self.parent.sprite.is_alive = False
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} 的残骸 "
        self.parent.sprite.render_order = RenderOrder.CORPSE
        self.engine.message_log.add_message(death_message, death_message_color)

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
