from entities import actors 
from entities import items
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


if __name__ == '__main__':
    print(entity_dict)
