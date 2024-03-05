
from __future__ import annotations

from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from entities.gear import GearParts

if TYPE_CHECKING:
    from entities.entity import Actor
    from entities.gear import Gear


class Equipment(BaseComponent):
    parent: Actor  # type: ignore
    helmet = None
    body = None
    leg = None
    foot = None
    left_hand = None
    right_hand = None

    def __init__(self, parent):
        self.parent = parent

    @property
    def gears(self):
        return [
                ('helmet', self.helmet),
                ('body', self.body),
                ('leg', self.leg),
                ('foot', self.foot),
                ('letf_hand', self.left_hand),
                ('right_hand', self.right_hand),
                ]

    def wear(self, gear: Gear) -> None:
        if gear.part == GearParts.RIGHT_HAND:
            self.left_hand = gear
        self.engine.message_log.add_message(
            f"You're equipped with {gear.name}.")  # type: ignore

    def to_dict(self):
        pass

    def load_dict(self, d):
        pass
