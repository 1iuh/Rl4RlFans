
from __future__ import annotations

from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from entities.gear import GearParts

if TYPE_CHECKING:
    from entities.entity import Actor
    from entities.gear import Gear


class Equipment(BaseComponent):
    parent: Actor  # type: ignore
    body = None
    foot = None
    hands = None

    def __init__(self, parent):
        self.parent = parent

    def get_stat(self, name):
        value = 0
        if self.body is not None:
            value += getattr(self.body, name)
        if self.foot is not None:
            value += getattr(self.foot, name)
        if self.hands is not None:
            value += getattr(self.hands, name)
        return value

    @property
    def gears(self):
        return [
                ('hands', self.hands),
                ('body', self.body),
                ('foot', self.foot),
                ]

    def put_down(self, part):
        if part == GearParts.BODY:
            gear = self.body
            self.body = None
        elif part == GearParts.FOOT:
            gear = self.foot
            self.foot = None
        elif part == GearParts.HANDS:
            gear = self.hands
            self.hands = None
        self.parent.inventory.put_donw(gear)

    def put_on(self, gear: Gear) -> None:
        if gear.part == GearParts.HANDS:
            self.hands = gear
        elif gear.part == GearParts.BODY:
            self.body = gear
        elif gear.part == GearParts.FOOT:
            self.foot = gear

        gear.parent = self
        self.engine.message_log.add_message(
            f"You're equipped with {gear.name}.")  # type: ignore

    def to_dict(self):
        pass

    def load_dict(self, d):
        pass
