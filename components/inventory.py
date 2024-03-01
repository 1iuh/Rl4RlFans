from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entities.entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor # type: ignore

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"你把 {item.name} 丢在了地上.") # type: ignore

    def to_dict(self):
        return dict(
                capacity = self.capacity,
                items = [i.to_dict() for i in self.items]
                )

    def load_dict(self, d):
        self.capacity = d['capacity']
        # TODO
        items = d['items']
        return 
