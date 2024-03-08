from __future__ import annotations


import actions
import color
import components.inventory
import components.ai
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import AreaRangedAttackHandler, SingleRangedAttackHandler
from entities.factors.others import fireball_missile

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item  # type: ignore

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent, None)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)  # type: ignore


class GearConsumable(Consumable):

    def activate(self, action: actions.ItemAction) -> None:
        self.parent.put_on()
        self.consume()


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)
        self.engine.message_log.add_message(
            f"You use {self.parent.name}, record {amount_recovered} hp!",
            color.health_recovered,
        )
        self.consume()


class ManaRecoverConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.mana_recover(self.amount)
        self.engine.message_log.add_message(
            f"You use {self.parent.name}, record {amount_recovered} mp!",
            color.health_recovered,
        )
        self.consume()


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if (actor is not consumer
                    and self.parent.gamemap.visible[actor.x, actor.y]):
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"一根闪电箭击中 {target.name} , 造成 {self.damage} 伤害!"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("范围内没有敌人")


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "选择目的地.", color.needs_target
        )
        self.engine.event_handler = SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("不能选择看不见的地方")
        if not target:
            raise Impossible("只能选择敌人")
        if target is consumer:
            raise Impossible("不能选择自己")

        self.engine.message_log.add_message(
            f"{target.name} 迷惑了, 开始四处乱走！",
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai,
            turns_remaining=self.number_of_turns,
        )
        self.consume()


class FireballConsumable(Consumable):

    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "Choice target.", color.needs_target
        )
        self.engine.event_handler = AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You can`t see there.")
        missile = fireball_missile.copy()
        missile.x = action.entity.x
        missile.y = action.entity.y
        missile.target_xy = action.target_xy
        missile.damage = self.damage
        missile.radius = self.radius
        self.engine.game_map.spawn_entity(missile)
        self.consume()
        action = missile.ai.perform()
        action.perform()


class FireballSkillConsumable(Consumable):

    def __init__(self, base_damage: int, radius: int):
        self.base_damage = base_damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "Choice target.", color.needs_target
        )
        self.engine.event_handler = AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You can`t see there.")

        self.engine.message_log.add_message(
                f"{action.speed}: {action.entity.name} threw a fireball")

        missile = fireball_missile.copy()
        missile.x = action.entity.x
        missile.y = action.entity.y
        missile.target_xy = action.target_xy
        missile.damage = self.base_damage + self.parent.parent.fighter.magic
        missile.radius = self.radius
        self.engine.game_map.spawn_entity(missile)
        self.consume()
        action = missile.ai.perform()
        action.perform()
