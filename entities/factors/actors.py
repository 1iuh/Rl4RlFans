import sprites
from components import ai
from components import inventory
from ..actor import Actor
from components.fighter import Fighter
import constants


player = Actor(
        entity_id=0,
        name="you",
        ai_cls=ai.HostileEnemy,
        fighter=Fighter(hp=40, defense=3, power=10, speed=5, magic=0),
        inventory=inventory.Inventory(capacity=10),
        sprite_f=sprites.player_sprite,
        cate=-1
        )

monsters = []
entity_id = 1000

for sp in sprites.monster_sprites:
    name = sp.__name__.replace("_sprite", "").replace("_", " ")
    cate = constants.MonsterType.Minion
    if name in (
        'necromancer',
        'orc_shaman',
        'orc_warrior',
            ):
        cate = constants.MonsterType.Ranger
    elif name in (
        'muddy',
        'ogre',
        'wogol',
        'zombie',
            ):
        cate = constants.MonsterType.Tank

    elif name in (
        'ice_zombie',
        'masked_orc',
        'big_demon',
        'big_zombie',
            ):
        cate = constants.MonsterType.Assassin
    ai_cls = ai.HostileEnemy
    if cate == constants.MonsterType.Ranger:
        ai_cls = ai.RangeAttackEnemy
    actor = Actor(
         entity_id=entity_id,
         name=name,
         ai_cls=ai_cls,
         fighter=Fighter(hp=10, defense=4, power=5, speed=8, magic=3),
         inventory=inventory.Inventory(capacity=0),
         sprite_f=sp,
         cate=cate
         )
    monsters.append(actor)
    entity_id += 1

friends = []
entity_id = 2000

for sp in sprites.friends_sprites:
    name = sp.__name__.replace("_sprite", "").replace("_", " ")
    cate = constants.MonsterType.Tank
    ai_cls = ai.FriendsAI
    actor = Actor(
         entity_id=entity_id,
         name=name,
         ai_cls=ai_cls,
         fighter=Fighter(hp=10, defense=4, power=5, speed=8, magic=3),
         inventory=inventory.Inventory(capacity=0),
         sprite_f=sp,
         cate=cate
         )
    friends.append(actor)
    entity_id += 1
