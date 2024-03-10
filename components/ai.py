from __future__ import annotations

import numpy as np  # type: ignore
import tcod
import random
import constants
import actions 

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor
    from engine import Engine


class BaseAI:
    entity: Actor

    def __init__(self, entity):
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> actions.Action:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int):
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class MissileAI(BaseAI):

    def perform(self) -> actions.Action:
        if self.entity.distance2target() < constants.missile_move_speed:
            return actions.MissileActivateAction(self.entity, self.entity.target_xy)
        else:
            path = self.get_path_to(self.entity.target_xy[0],
                                    self.entity.target_xy[1])
            return actions.TPAction(self.entity, path[constants.missile_move_speed-1])


class VfxAI(BaseAI):

    def perform(self) -> actions.Action:
        return actions.MissileActivateAction(self.entity, (0, 0))


class HostileEnemy(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self) -> actions.Action:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return actions.MeleeAction(self.entity, dx, dy)

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return actions.MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            )

        return actions.WaitAction(self.entity)


class RangeAttackEnemy(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self) -> actions.Action:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 4:
                return actions.RangeAttackAction(self.entity, dx, dy)

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return actions.MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            )

        return actions.WaitAction(self.entity)


class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble around aimlessly for a given number of turns,
    then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
        self, entity: Actor, previous_ai: Optional[BaseAI],
        turns_remaining: int
    ):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> actions.Action:
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"{self.entity.name} 不再困惑."
            )
            self.entity.ai = self.previous_ai
            return self.entity.ai.perform()
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return actions.BumpAction(self.entity, direction_x, direction_y)
