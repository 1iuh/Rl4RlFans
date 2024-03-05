from entities import actors
from entities import items
from entities import others
from entities.entity import Entity


def add_entity_to_dict(module):
    for attr_str in dir(module):
        if attr_str.startswith('__'):
            continue
        entity = getattr(module, attr_str)
        if isinstance(entity, Entity):
            entity_dict[entity.entity_id] = entity


entity_dict = {}
add_entity_to_dict(actors)
add_entity_to_dict(items)
add_entity_to_dict(others)


if __name__ == '__main__':
    entity_dict
    print(entity_dict[9000].copy())
