from __future__ import annotations

from typing import TYPE_CHECKING

import arcade

if TYPE_CHECKING:
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(current_value: int, maximum_value: int, total_width: int) -> None:

    bar_width = int(float(current_value) / maximum_value * total_width)

    arcade.draw_rectangle_outline(
        100, 800, total_width*12, 20, arcade.color.AERO_BLUE)  # type: ignore
    if bar_width > 0:
        arcade.draw_rectangle_filled(
            100, 800, bar_width*12, 20, arcade.color.RED_ORANGE)  # type: ignore
    # arcade.draw_text(f"HP:{current_value}/{maximum_value}", 70, 794)
