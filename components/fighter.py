from __future__ import annotations

from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler

from typing import TYPE_CHECKING
from render_order import RenderOrder
import color

if TYPE_CHECKING:
   from entity import Actor

class Fighter(BaseComponent):

    parent: Actor # type: ignore

    def __init__(self, hp: int, defense: int, power: int, speed: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
        self.speed: int = speed

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

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
            death_message = "你 死掉了！"
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
