from ..gear import Gear, GearParts
from components.consumable import GearConsumable
import sprites


sword = Gear(
        part=GearParts.RIGHT_HAND,
        consumable=GearConsumable(),
        entity_id=10000,
        name="sword ",
        sprite_f=sprites.sword_sprite,
        )

shield = Gear(
        part=GearParts.LEFT_HAND,
        consumable=GearConsumable(),
        entity_id=10001,
        name="shield",
        sprite_f=sprites.potion_1,
        )

boots = Gear(
        part=GearParts.FOOT,
        consumable=GearConsumable(),
        entity_id=10002,
        name="boots",
        sprite_f=sprites.potion_2,
        )

helmet = Gear(
        part=GearParts.HELMET,
        consumable=GearConsumable(),
        entity_id=10003,
        name="helmet",
        sprite_f=sprites.potion_2,
        )
