from ..entity import Item
from components import consumable
import sprites


health_potion = Item(
        entity_id=6000,
        name="health potion",
        desc='recover 20% hp',
        consumable=consumable.HealingConsumable(amount=20),
        sprite_f=sprites.health_potion,
        )

mana_potion = Item(
        entity_id=6001,
        name="mana potion",
        desc='recover 20% mp',
        consumable=consumable.ManaRecoverConsumable(amount=20),
        sprite_f=sprites.mana_potion,
        )

all_item = [health_potion, mana_potion]

lightning_scroll = Item(
        entity_id=6002,
        name="闪电卷轴",
        desc='null',
        consumable=consumable.LightningDamageConsumable(damage=20,
                                                        maximum_range=5),
        sprite_f=sprites.health_potion,
        )

confusion_scroll = Item(
        entity_id=6003,
        name="迷惑卷轴",
        desc='null',
        consumable=consumable.ConfusionConsumable(number_of_turns=10),
        sprite_f=sprites.health_potion,
        )

fireball_scroll = Item(
        entity_id=6004,
        name="火球卷轴",
        desc='null',
        consumable=consumable.FireballConsumable(20, 2),
        sprite_f=sprites.health_potion,
        )
