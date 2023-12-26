from entity import Actor, Item
from components.fighter import Fighter
from components.consumable import HealingConsumable
from components.ai import HostileEnemy
from components.inventory import Inventory

player = Actor(
   char="@",
   color=(255, 255, 255),
   name="你",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=30, defense=2, power=5),
   inventory=Inventory(capacity=26),
)

a_tree = Actor(
   char="T",
   color=(3, 100, 30),
   name="阿树",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=10, defense=4, power=1),
   inventory=Inventory(capacity=0),
)

twoflower = Actor(
   char="T",
   color=(0, 0, 255),
   name="蓝猫",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=15, defense=0, power=3),
   inventory=Inventory(capacity=0),
)

sagancharum = Actor(
   char="P",
   color=(3, 252, 65),
   name="甘蔗",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=18, defense=2, power=3),
   inventory=Inventory(capacity=0),
)

all_entities = (a_tree, twoflower, sagancharum) 

health_potion = Item(
   char="!",
   color=(127, 0, 255),
   name="生命药水",
   consumable=HealingConsumable(amount=4),
)
