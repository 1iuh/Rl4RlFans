from entities.skill import Skill
from components import consumable


def fireball_skill(actor):
    return Skill('Fireball',
                 '3+Magic',
                 5,
                 consumable.FireballSkillConsumable(3, 2), actor)


def teleportation_skill(actor):
    return Skill('Teleportation',
                 '0',
                 4, consumable.TPConsumable(5), actor)


def lightning_bolt_skill(actor):
    return Skill('lightning bolt',
                 '5+Magic*2',
                 4,
                 consumable.LightningBoltConsumable(5, 5), actor)
