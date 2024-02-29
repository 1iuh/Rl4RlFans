from entity import Actor, Item, Missile
from components.fighter import Fighter
from components import consumable
from components.ai import HostileEnemy
from components.inventory import Inventory
import sprites

player = Actor(
        entity_id=0,
        name="你",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=40, defense=2, power=10, speed=5),
        inventory=Inventory(capacity=26),
        sprite=sprites.player_sprite()
        )

a_tree = Actor(
        entity_id=1000,
        name="阿树",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=10, defense=4, power=1, speed=1),
        inventory=Inventory(capacity=0),
        sprite=sprites.big_zombie(),
        )

twoflower = Actor(
        entity_id=1001,
        name="蓝猫",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=15, defense=0, power=3, speed=10),
        inventory=Inventory(capacity=0),
        sprite=sprites.big_demon(),
        )

sagancharum = Actor(
        entity_id=1002,
        name="甘蔗",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=3),
        inventory=Inventory(capacity=0),
        sprite=sprites.chort(),
        )
feishiko = Actor(
        entity_id=1003,
        name="feishiko",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=4),
        inventory=Inventory(capacity=0),
        sprite=sprites.feishiko(),
        )
toufu = Actor(
        entity_id=1004,
        name="麻婆豆腐",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=5),
        inventory=Inventory(capacity=0),
        sprite=sprites.toufu(),
        )
silencess = Actor(
        entity_id=1005,
        name="言静",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=7),
        inventory=Inventory(capacity=0),
        sprite=sprites.silencess(),
        )

superlight = Actor(
        entity_id=1006,
        name="科学超电灯泡",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=8),
        inventory=Inventory(capacity=0),
        sprite=sprites.superlight(),
        )

all_entities = (a_tree, twoflower, sagancharum, feishiko, toufu, silencess, superlight) 

health_potion = Item(
        entity_id=6000,
        name="生命药水",
        consumable=consumable.HealingConsumable(amount=4),
        sprite=sprites.potion_0(),
        )

health_potion = Item(
        entity_id=6001,
        name="生命药水",
        consumable=consumable.HealingConsumable(amount=4),
        sprite=sprites.potion_0(),
        )

lightning_scroll = Item(
        entity_id=6002,
        name="闪电卷轴",
        consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
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

