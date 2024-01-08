from __future__ import annotations

from tcod.map import compute_fov
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar
from entity_factories import fireball_scroll
import exceptions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler
    from actions import Action


class Engine:

    game_map: GameMap

    def __init__(self, player: Actor):

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.action_queue: list[Action] = []

    def handle_enemy_turns(self) -> None:

        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    self.action_queue.append(entity.ai.perform)
                except exceptions.Impossible:
                    pass

    def on_start(self):

        fireball_scroll.parent = self.player.inventory
        self.player.inventory.items.append(fireball_scroll)
        self.player.inventory.items.append(fireball_scroll)
        self.player.inventory.items.append(fireball_scroll)
        self.player.inventory.items.append(fireball_scroll)
        self.player.inventory.items.append(fireball_scroll)
        self.player.inventory.items.append(fireball_scroll)
        self.player.inventory.items.append(fireball_scroll)

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""

        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self) -> None:

        self.game_map.render()
        self.message_log.render(x=14, y=720, lines=10)
        render_bar(
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=12,
        )
