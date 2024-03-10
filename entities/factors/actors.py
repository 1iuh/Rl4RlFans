import sprites
from components import ai
from components import inventory
from ..actor import Actor
from components.fighter import Fighter


player = Actor(
        entity_id=0,
        name="you",
        ai_cls=ai.HostileEnemy,
        fighter=Fighter(hp=40, defense=20, power=80, speed=5, magic=0),
        inventory=inventory.Inventory(capacity=12),
        sprite_f=sprites.player_sprite
        )

monsters = []
entity_id = 1000

for sp in sprites.monster_sprites:
    name = sp.__name__.replace("_sprite", "").replace("_", " ")
    actor = Actor(
         entity_id=entity_id,
         name=name,
         ai_cls=ai.HostileEnemy,
         fighter=Fighter(hp=10, defense=4, power=5, speed=8, magic=3),
         inventory=inventory.Inventory(capacity=0),
         sprite_f=sp
         )
    monsters.append(actor)
    entity_id += 1


"""
a_tree = Actor(
        entity_id=1000,
        name="atree",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=10, defense=4, power=5, speed=8),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.big_zombie,
        )

twoflower = Actor(
        entity_id=1001,
        name="twoflower",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=15, defense=0, power=3, speed=10),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.big_demon,
        )

sagancharum = Actor(
        entity_id=1002,
        name="sagancharum",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=3),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.chort,
        )
feishiko = Actor(
        entity_id=1003,
        name="feishiko",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=4),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.feishiko,
        )
toufu = Actor(
        entity_id=1004,
        name="toufu",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=5),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.toufu,
        )
silencess = Actor(
        entity_id=1005,
        name="silencess",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=7),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.silencess,
        )

superlight = Actor(
        entity_id=1006,
        name="superlight",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=18, defense=2, power=3, speed=8),
        inventory=Inventory(capacity=0),
        sprite_f=sprites.superlight,
        )
"""
