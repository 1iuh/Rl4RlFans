from __future__ import annotations

from typing import TYPE_CHECKING

import arcade

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar( current_value: int, maximum_value: int, total_width: int) -> None:

    bar_width = int(float(current_value) / maximum_value * total_width)

    arcade.draw_rectangle_outline(100, 800, total_width*12, 20, arcade.color.AERO_BLUE) # type: ignore
    if bar_width > 0:
        arcade.draw_rectangle_filled(100, 800, bar_width*12, 20, arcade.color.RED_ORANGE) # type: ignore
    arcade.draw_text(f"HP:{current_value}/{maximum_value}", 70, 794)

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
    ) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)
