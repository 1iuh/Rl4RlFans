
import constants
import random


class FriendChoice:

    def __init__(self, desc, callback):
        self.desc = desc
        self.callback = callback

    def perform(self):
        self.callback()


friend_choices = [
        FriendChoice('There are too few monsters.',
                     lambda: constants.max_monsters_per_room + 1),
        FriendChoice('There are too much monsters',
                     lambda: constants.max_monsters_per_room + 1),
        FriendChoice('Too few items, more of them.',
                     lambda: constants.item_generate_rate + 0.1),
        FriendChoice('Too little gear.',
                     lambda: constants.gear_generate_rate + 0.1),
        FriendChoice('Monsters drop too little gear.',
                     lambda: constants.monster_drop_rate + 0.1),
        FriendChoice('More high quality gear.',
                     lambda: constants.enchant_bonus + 0.1),
        FriendChoice('More powerful gear enchantments.',
                     lambda: constants.enchant_stats_bonus + 0.1),
        FriendChoice('The attributes of the gear suck.',
                     lambda: constants.gear_base_stat_bonus + 0.1),
        FriendChoice('The monsters are too weak.',
                     lambda: constants.monster_stat_bonus + 0.1),
        FriendChoice('The monsters are too strong.',
                     lambda: constants.monster_stat_bonus - 0.1),
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
