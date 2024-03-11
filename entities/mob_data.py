import constants

mob_data = {
        constants.MonsterType.Minion: {
            'hp': 12,
            'power': 6,
            'defense': 3,
            'magic': 0,
            'speed': 5,
            },
        constants.MonsterType.Ranger: {
            'hp': 8,
            'power': 0,
            'defense': 2,
            'magic': 4,
            'speed': 3,
            },
        constants.MonsterType.Tank: {
            'hp': 16,
            'power': 6,
            'defense': 4,
            'magic': 0,
            'speed': 1,
            },
        constants.MonsterType.Assassin: {
            'hp': 10,
            'power': 10,
            'defense': 2,
            'magic': 0,
            'speed': 10,
            },
        }

monster_growth_base_rate = {
        'power': 1.2,
        'hp': 1.2,
        'magic': 1.2,
        'defense': 1.2,
        'speed': 1.1,
    }

elite_stat_rate = 1.3
