from __future__  import annotations

import color
import exceptions

from typing import TYPE_CHECKING, Optional, Tuple


if TYPE_CHECKING:
    from entity import Actor, Item
    from engine import Engine

class Action:

    entity: Actor
    speed: int =  1

    def __init__(self, entity):
        super().__init__()
        self.entity = entity

    @property
    def engine(self)->Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):

    speed: int =  3

    def __init__(self, entity, dx, dy):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self):
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self):
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
       raise NotImplementedError()


class MeleeAction(ActionWithDirection):

    speed: int =  8

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")
 
        damage = self.entity.fighter.power - target.fighter.defense
 
        attack_desc = f"{self.entity.name.capitalize()} 使用拳头攻击了 {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} 造成了 {damage} 物理伤害.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} 但是毫无效果.", attack_color
            )


class MovementAction(ActionWithDirection):

    def perform(self):
        dest_x, dest_y = self.dest_xy
        

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("那里没路。")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is out of bounds.
            raise exceptions.Impossible("那里没路。")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("那里没路。")

        self.entity.move(self.dx, self.dy)


class WaitAction(Action):
    speed: int = 0

    def perform(self):
        pass


class BumpAction(ActionWithDirection):

   def perform(self):
    if self.target_actor:
        return MeleeAction(self.entity, self.dx, self.dy).perform()
    else:
        return MovementAction(self.entity, self.dx, self.dy).perform()


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        self.item.consumable.activate(self)


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("背包满了")

                item.despawn(self.engine.game_map)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"你 拾取了 {item.name}!")
                return

        raise exceptions.Impossible("地上没东西！")


class DropItem(ItemAction):

    def perform(self) -> None:
        self.entity.inventory.drop(self.item)
