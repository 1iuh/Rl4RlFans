
import random
import env_val


class FriendChoice:

    def __init__(self, desc, callback):
        self.desc = desc
        self.callback = callback

    def perform(self):
        self.callback()
        

def change_env_val(env_name, val):
    v = getattr(env_val, env_name) + val
    setattr(env_val, env_name, v)

friend_choices = [
        FriendChoice('Let there be more monsters.',
                     lambda: change_env_val('max_monsters_per_room', 1)),
        FriendChoice('Make the monsters less.',
                     lambda: change_env_val('max_monsters_per_room', -1)),
        FriendChoice('Let potions be more.',
                     lambda: change_env_val('item_generate_rate', 0.1)),
        FriendChoice('Let gear be more.',
                     lambda: change_env_val('gear_generate_rate', 0.1)),
        FriendChoice('Make monsters drop more gear.',
                     lambda: change_env_val('monster_drop_rate', 0.1)),
        FriendChoice('More high quality gear.',
                     lambda: change_env_val('enchant_bonus', 0.1)),
        FriendChoice('More powerful gear enchantments.',
                     lambda: change_env_val('enchant_stats_bonus', 0.1)),
        FriendChoice('Make the gear`s attributes better.',
                     lambda: change_env_val('gear_base_stat_bonus', 0.1)),
        FriendChoice('Make the monsters stronger.',
                     lambda: change_env_val('monster_stat_bonus', 0.1)),
        FriendChoice('Make the monsters weaker.',
                     lambda: change_env_val('monster_stat_bonus', -0.1)),
        FriendChoice('Win the game early.',
                     lambda: change_env_val('end_level', -1)),
        FriendChoice('Win the game late.',
                     lambda: change_env_val('end_level', 1)),
        ]


def got_2_choices():
    c1 = random.choice(friend_choices)
    c2 = random.choice(friend_choices)
    while c1 == c2:
        c2 = random.choice(friend_choices)
    return [
            c1,
            c2
            ]
