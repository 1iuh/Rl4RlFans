from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
import components.ai
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import AreaRangedAttackHandler, SingleRangedAttackHandler

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item # type: ignore

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

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
            inventory.items.remove(entity) # type: ignore


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"你 使用了 {self.parent.name}, 恢复了 {amount_recovered} 生命值!",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"你的生命值是满的.")


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
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
            entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
        )
        self.consume()


class FireballConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "选择目标.", color.needs_target
        )
        self.engine.event_handler = AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy
        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("不能选择没有视野的地方.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"{actor.name} 被炽热的爆炸吞噬, 受到了 {self.damage} 伤害!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("范围内没有目标")
        self.consume()
