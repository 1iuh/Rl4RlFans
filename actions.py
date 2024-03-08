from __future__ import annotations

import color
import exceptions

from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from entities.entity import Actor, Item
    from entities.skill import Skill
    from entities.gear import Gear
    from engine import Engine


class Action:

    entity: Actor

    def __init__(self, entity):
        super().__init__()
        self.entity = entity

    @property
    def speed(self):
        return self.entity.fighter.speed

    @property
    def engine(self) -> Engine:
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
        return self.engine.game_map.get_blocking_entity_at_location(
                *self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):

    def perform(self) -> None:

        if not self.entity.fighter.is_alive:
            return

        target = self.target_actor

        if not target:
            attack_color = color.player_atk
            self.engine.message_log.add_message(
                f"{self.entity.name} miss", attack_color
            )
            return

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.speed}: {self.entity.name} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class MovementAction(ActionWithDirection):

    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            self.engine.message_log.add_message("No way")
            return
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is out of bounds.
            self.engine.message_log.add_message("No way")
            return
        if self.engine.game_map.get_blocking_entity_at_location(
                dest_x, dest_y):
            # Destination is out of bounds.
            self.engine.message_log.add_message("No way")
            return

        attack_desc = f"{self.speed}: {self.entity.name} moved."
        self.engine.message_log.add_message(attack_desc)
        self.entity.move(self.dx, self.dy)


class WaitAction(Action):

    @property
    def speed(self):
        return 0

    def perform(self):
        pass


class BumpAction(ActionWithDirection):

    def perform(self):
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class SkillAction(Action):
    def __init__(self, entity: Actor, skill: Skill, target_xy):
        super().__init__(entity)
        self.skill = skill
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability,
        this action will be given to provide context.
        """
        self.skill.consumable.activate(self)


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy):
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
        """Invoke the items ability,
        this action will be given to provide context.
        """
        self.item.consumable.activate(self)


class TPAction(Action):

    def __init__(self, entity, target_xy):
        super().__init__(entity)
        self.target_xy = target_xy

    def perform(self) -> None:
        self.entity.x = self.target_xy[0]
        self.entity.y = self.target_xy[1]


class MissileActivateAction(Action):

    @property
    def speed(self):
        return 999

    def __init__(self, entity, target_xy):
        super().__init__(entity)
        self.target_xy = target_xy

    def perform(self) -> None:
        self.entity.activate()


class PutDownAction(Action):

    def __init__(self, actor, gear: Gear):
        super().__init__(actor)
        self.gear = gear

    def perform(self) -> None:
        self.gear.put_down()


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
                    raise exceptions.Impossible("inventory is full.")
                self.engine.game_map.despawn_entity(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"you pickup {item.name}!")
                return

        self.engine.message_log.add_message(
                "there is nothing!")


class DropItem(ItemAction):

    def __init__(self, actor, item):
        super().__init__(actor, item, (0, 0))

    def perform(self) -> None:
        self.entity.inventory.drop(self.item)
