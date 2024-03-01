from .entity import Item
from components import consumable
import sprites


health_potion = Item(
        entity_id=6000,
        name="生命药水",
        consumable=consumable.HealingConsumable(amount=4),
        sprite=sprites.potion_0(),
        )

lightning_scroll = Item(
        entity_id=6002,
        name="闪电卷轴",
        consumable=consumable.LightningDamageConsumable(damage=20,
                                                        maximum_range=5),
        sprite=sprites.potion_1(),
        )

confusion_scroll = Item(
        entity_id=6003,
        name="迷惑卷轴",
        consumable=consumable.ConfusionConsumable(number_of_turns=10),
        sprite=sprites.potion_2(),
        )

fireball_scroll = Item(
        entity_id=6004,
        name="火球卷轴",
        consumable=consumable.FireballConsumable(20, 2),
        sprite=sprites.potion_2(),
        )
