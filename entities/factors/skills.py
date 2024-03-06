from entities.skill import Skill
from components.consumable import FireballSkillConsumable


def fireball_skill(actor):
    return Skill('Fireball', 5, FireballSkillConsumable(3, 2), actor)
