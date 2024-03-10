
def sword_data(level):
    return {'power': 5 + 3 * (level-1)}


def wand_data(level):
    return {
        'power': 1 + 1 * (level-1),
        'magic': 3 + 2 * (level-1),
    }


def armor_data(level):
    return {
        'defense': 3 + 2 * (level-1),
        'max_hp': 3 + 3 * (level-1),
    }


def colth_data(level):
    return {
        'magic': 1 + 1 * (level-1),
        'max_mp': 3 + 4 * (level-1),
    }


def iron_boots_data(level):
    return {
        'defense': 1 + 2 * (level-1),
    }


def cloth_boots_data(level):
    return {
        'speed': 1 + 2 * (level-1),
    }
