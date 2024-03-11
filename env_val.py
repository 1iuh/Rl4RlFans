
max_monsters_per_room = 2
max_items_per_room = 2
item_generate_rate = 0.25
gear_generate_rate = 0.15
monster_drop_rate = 0.4
enchant_bonus = 1
enchant_stats_bonus = 1
gear_base_stat_bonus = 1
monster_stat_bonus = 1
end_level = 5


def dict_dump():
    return dict(
        max_monsters_per_room = max_monsters_per_room,
        max_items_per_room = max_items_per_room,
        item_generate_rate = item_generate_rate,
        gear_generate_rate = gear_generate_rate,
        monster_drop_rate = monster_drop_rate,
        enchant_bonus = enchant_bonus,
        enchant_stats_bonus = enchant_stats_bonus,
        gear_base_stat_bonus = gear_base_stat_bonus,
        monster_stat_bonus = monster_stat_bonus,
        end_level = end_level,
    )

def load_dict(d):
    if d.get('max_monsters_per_room') is None:
        return
    global max_monsters_per_room
    global max_items_per_room
    global item_generate_rate
    global gear_generate_rate
    global monster_drop_rate
    global enchant_bonus
    global enchant_stats_bonus
    global gear_base_stat_bonus
    global monster_stat_bonus
    global end_level
    max_monsters_per_room = d['max_monsters_per_room']
    max_items_per_room = d['max_items_per_room']
    item_generate_rate = d['item_generate_rate']
    gear_generate_rate = d['gear_generate_rate']
    monster_drop_rate = d['monster_drop_rate']
    enchant_bonus = d['enchant_bonus']
    enchant_stats_bonus = d['enchant_stats_bonus']
    gear_base_stat_bonus = d['gear_base_stat_bonus']
    monster_stat_bonus = d['monster_stat_bonus']
    end_level = d['end_level']