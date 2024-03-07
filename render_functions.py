from __future__ import annotations

from typing import TYPE_CHECKING
import constants

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


def render_bar(current_value, maximum_value, total_width,
               color, start_y, name):

    bar_width = int(float(current_value) / maximum_value * total_width)

    arcade.draw_rectangle_outline(
        90, start_y, total_width*12, 20, arcade.color.AERO_BLUE)
    if bar_width > 0:
        arcade.draw_rectangle_filled(
            90, start_y, bar_width*12, 20, color)  # type: ignore
    arcade.draw_text(f"{name}:{current_value}/{maximum_value}", 60, start_y,
                     anchor_y='center')


def render_mob_bar(current_value, maximum_value, start_x, start_y):

    bar_width = int(float(current_value) / maximum_value * constants.grid_size)
    y_offset = constants.grid_size / 2

    arcade.draw_rectangle_filled(
        start_x, start_y + y_offset,
        bar_width, 2, arcade.color.RED)  # type: ignore
