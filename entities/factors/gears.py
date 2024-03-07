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

wand = Gear(
        part=GearParts.HANDS,
        consumable=GearConsumable(),
        entity_id=10001,
        name="wand",
        sprite_f=sprites.wand_sprite,
        stats=gear_data.wand_data
        )


iron_armor = Gear(
        part=GearParts.BODY,
        consumable=GearConsumable(),
        entity_id=10002,
        name="iron armor",
        sprite_f=sprites.iron_armor_sprite,
        stats=gear_data.armor_data
        )

armor = Gear(
        part=GearParts.BODY,
        consumable=GearConsumable(),
        entity_id=10003,
        name="armor",
        sprite_f=sprites.cloth,
        stats=gear_data.colth_data
        )

iron_boots = Gear(
        part=GearParts.FOOT,
        consumable=GearConsumable(),
        entity_id=10004,
        name="iron boots",
        sprite_f=sprites.iron_boot_sprite,
        stats=gear_data.iron_boots_data
        )

boots = Gear(
        part=GearParts.FOOT,
        consumable=GearConsumable(),
        entity_id=10005,
        name="boots",
        sprite_f=sprites.boot,
        stats=gear_data.cloth_boots_data
        )

all_gears = [
        sword,
        wand,
        armor,
        boots,
        iron_armor,
        iron_boots,
        ]
