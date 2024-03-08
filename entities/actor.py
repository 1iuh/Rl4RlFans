from __future__ import annotations

from entities.entity import Entity
from components.equipment import Equipment
from entities.factors import skills
from entities.mob_data import mob_data

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from components.inventory import Inventory
    from components.fighter import Fighter
    from sprites import ActorSprite


class Actor(Entity):

    sprite: ActorSprite
    skills: list
    level = 1

    def __init__(self,
                 *,
                 entity_id: int = 0,
                 x: int = 0,
                 y: int = 0,
                 name: str = "<Unnamed>",
                 sprite_f,
                 ai_cls,
                 fighter: Fighter,
                 inventory: Inventory,
                 ):

        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            name=name,
            blocks_movement=True,
            sprite_f=sprite_f,
        )

        self.ai = ai_cls(self)
        self.fighter = fighter
        self.fighter.parent = self
        self.inventory = inventory
        self.inventory.parent = self
        self.equipment = Equipment(self)

        self.skills = []
        self.skills.append(skills.fireball_skill(self))
        self.skills.append(skills.teleportation_skill(self))
        self.skills.append(skills.lightning_bolt_skill(self))

    def copy(self):
        clone = super().copy()
        if self.entity_id == 0:
            return clone
        clone.rand()
        return clone

    def rand(self):
        for attr, value in mob_data[self.level].items():
            setattr(self.fighter, '_'+attr, value)
        self.fighter._max_hp = self.fighter._hp
        # if len(self.desc) > 0:
        #     self.desc = ','.join([self.desc, f"{attr}+{value}"])
        # else:
        #     self.desc = f"{attr}+{value}"

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
            name=self.name,
            fighter=self.fighter.to_dict(),
            inventory=self.inventory.to_dict(),
        )

    def load_dict(self, d):
        self.entity_id = d['entity_id']
        self.x = d['x']
        self.y = d['y']
        self.name = d['name']
        self.fighter.load_dict(d['fighter'])
        self.inventory.load_dict(d['inventory'])
        return
