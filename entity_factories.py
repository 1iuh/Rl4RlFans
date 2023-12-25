from entity import Actor
from components.fighter import Fighter
from components.ai import HostileEnemy

player = Actor(
   char="@",
   color=(255, 255, 255),
   name="Player",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=30, defense=2, power=5),
)

a_tree = Actor(
   char="T",
   color=(3, 252, 65),
   name="阿树",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=10, defense=5, power=1),
)

twoflower = Actor(
   char="T",
   color=(0, 0, 255),
   name="蓝猫",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=15, defense=0, power=3),
)

sagancharum = Actor(
   char="P",
   color=(3, 252, 65),
   name="甘蔗",
   ai_cls=HostileEnemy,
   fighter=Fighter(hp=18, defense=2, power=3),
)

all_entities = (a_tree, twoflower, sagancharum) 
