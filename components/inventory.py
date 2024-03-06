from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent
import entities
import copy

if TYPE_CHECKING:
    from entities.entity import Actor, Item
    from entities.gear import Gear


class Inventory(BaseComponent):
    parent: Actor  # type: ignore

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def put_on(self, gear: Gear) -> None:
        self.items.remove(gear)
        self.parent.equipment.put_on(gear)

    def put_donw(self, gear: Gear) -> None:
        gear.parent = self
        self.items.append(gear)

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map,
        at the player's current location.
        """
        self.items.remove(item)
        item.x = self.parent.x
        item.y = self.parent.y
        self.gamemap.spawn_entity(item)
        self.engine.message_log.add_message(
            f"你把 {item.name} 丢在了地上.")  # type: ignore

    def to_dict(self):
        return dict(
            capacity=self.capacity,
            items=[i.to_dict() for i in self.items]
        )

    def load_dict(self, d):
        self.capacity = d['capacity']
        for item_data in d['items']:
            entity = entities.entity_dict[item_data['entity_id']]
            clone = copy.deepcopy(entity)
            clone.parent = self
            self.items.append(clone)
