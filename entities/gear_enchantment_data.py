import env_val
base_enchant_rate = {
        1: 0.4,
        2: 0.2,
        3: 0.1,
    }


def rate_of_enchant(count):
    rate = base_enchant_rate[count]
    return rate * env_val.enchant_bonus


base_enchant_stat = {
        'power': 2,
        'defense': 2,
        'magic': 2,
        'max_hp': 3,
        'max_mp': 4,
        'speed': 1
    }


def enchant_stat_value(level: int, stat_key):
    base = base_enchant_stat[stat_key]
    val = int(base * (env_val.enchant_stats_bonus ** level))
    return val
