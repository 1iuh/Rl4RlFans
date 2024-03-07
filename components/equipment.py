
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
            value += self.body.get_stats(name)
        if self.foot is not None:
            value += self.foot.get_stats(name)
        if self.hands is not None:
            value += self.hands.get_stats(name)
        return value

    @property
    def gears(self):
        return [
                ('Hands', self.hands),
                ('Body', self.body),
                ('Foot', self.foot),
                ]

    def put_down(self, gear):
        if gear.part == GearParts.BODY:
            gear = self.body
            self.body = None
        elif gear.part == GearParts.FOOT:
            gear = self.foot
            self.foot = None
        elif gear.part == GearParts.HANDS:
            gear = self.hands
            self.hands = None
        self.parent.inventory.put_donw(gear)

    def put_on(self, gear: Gear) -> None:
        if gear.part == GearParts.HANDS:
            if self.hands is not None:
                self.put_down(self.hands)
            self.hands = gear
        elif gear.part == GearParts.BODY:
            if self.body is not None:
                self.put_down(self.body)
            self.body = gear
        elif gear.part == GearParts.FOOT:
            if self.foot is not None:
                self.put_down(self.foot)
            self.foot = gear

        gear.parent = self
        self.engine.message_log.add_message(
            f"You're equipped with {gear.name}.")  # type: ignore

    def to_dict(self):
        pass

    def load_dict(self, d):
        pass
