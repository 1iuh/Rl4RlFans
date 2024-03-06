from ..gear import Gear, GearParts
from components.consumable import GearConsumable
from entities import gear_data
import sprites


sword = Gear(
        part=GearParts.HANDS,
        consumable=GearConsumable(),
        entity_id=10000,
        name="sword",
        sprite_f=sprites.sword_sprite,
        stats=gear_data.sword_data
        )

boots = Gear(
        part=GearParts.FOOT,
        consumable=GearConsumable(),
        entity_id=10002,
        name="iron boots",
        sprite_f=sprites.iron_boot_sprite,
        stats=gear_data.iron_boots_data
        )

plate_mail = Gear(
        part=GearParts.BODY,
        consumable=GearConsumable(),
        entity_id=10003,
        name="iron armor",
        sprite_f=sprites.iron_armor_sprite,
        stats=gear_data.armor_data
        )
