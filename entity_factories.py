from entity import Actor, Item
from components.fighter import Fighter
from components import consumable
from components.ai import HostileEnemy
from components.inventory import Inventory
import tilesets

player = Actor(
        char="@",
        color=(255, 255, 255),
        name="你",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=30, defense=2, power=5),
        inventory=Inventory(capacity=26),
        hasAnimation=True,
        sprite=tilesets.player
        )

a_tree = Actor(
        char="T",
        color=(3, 100, 30),
        name="阿树",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=10, defense=4, power=1),
        inventory=Inventory(capacity=0),
        sprite=tilesets.player1,
        )

twoflower = Actor(
        char="T",
        color=(0, 0, 255),
        name="蓝猫",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=15, defense=0, power=3),
        inventory=Inventory(capacity=0),
        sprite=tilesets.player2,
        )

sagancharum = Actor(
        char="P",
        color=(3, 252, 65),
        name="甘蔗",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3),
        inventory=Inventory(capacity=0),
        sprite=tilesets.player3,
        )

all_entities = (a_tree, twoflower, sagancharum) 

health_potion = Item(
        char="!",
        color=(127, 0, 255),
        name="生命药水",
        consumable=consumable.HealingConsumable(amount=4),
        sprite=tilesets.player,
        )

health_potion = Item(
        char="!",
        color=(127, 0, 255),
        name="生命药水",
        consumable=consumable.HealingConsumable(amount=4),
        sprite=tilesets.player,
        )

lightning_scroll = Item(
        char="~",
        color=(255, 255, 0),
        name="闪电卷轴",
        consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
        sprite=tilesets.player,
        )

confusion_scroll = Item(
        char="~",
        color=(207, 63, 255),
        name="迷惑卷轴",
        consumable=consumable.ConfusionConsumable(number_of_turns=10),
        sprite=tilesets.player,
        )

fireball_scroll = Item(
        char="~",
        color=(255, 0, 0),
        name="火球卷轴",
        consumable=consumable.FireballConsumable(20, 2),
        sprite=tilesets.player,
        )
