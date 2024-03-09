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
                     anchor_y='center', font_name=constants.font_name)


def render_mob_bar(current_value, maximum_value, start_x, start_y):

    bar_width = int(float(current_value) / maximum_value * constants.grid_size)
    y_offset = constants.grid_size / 2

    arcade.draw_rectangle_filled(
        start_x, start_y + y_offset,
        bar_width, 2, arcade.color.RED)  # type: ignore


title = None
content = None
notice_window_title = None
notice_window_content = None


def render_notice_window(title_txt, content_txt, offset_x=0,
                         height=200, align='center', margin_top=140):

    global notice_window_title
    global notice_window_content

    center_x = constants.screen_center_x - constants.inventory_window_width/2
    center_x = int(center_x) + offset_x
    if notice_window_title is None:
        notice_window_title = arcade.Text(
            "",
            center_x,
            (int(constants.screen_center_y
                 + constants.inventory_window_height/2)
             - constants.font_line_height),
            arcade.color.WHITE,  # type: ignore
            20,
            align='center',
            width=constants.inventory_window_width,
            font_name='LT Binary Neue Round',
        )
    if notice_window_content is None:
        notice_window_content = arcade.Text(
            "",
            center_x,
            int(constants.screen_center_y + constants.inventory_window_height /
                2) - constants.font_line_height*1,
            arcade.color.WHITE,  # type: ignore
            constants.font_size,
            multiline=True,
            align=align,
            width=constants.inventory_window_width,
            font_name='LT Binary Neue Round',
        )

    notice_window_title.x = center_x
    notice_window_content.x = center_x
    notice_window_title.text = title_txt
    notice_window_content.text = content_txt
    notice_window_title.y = int(constants.screen_center_y + height / 2) - 60
    notice_window_content.y = int(constants.screen_center_y + height / 2)
    notice_window_content.y -= margin_top
    notice_window_content.align = align

    arcade.draw_rectangle_filled(
        center_x+constants.inventory_window_width/2,
        constants.screen_center_y,
        constants.inventory_window_width,
        height,
        arcade.color.BLACK_LEATHER_JACKET

    )

    arcade.draw_rectangle_outline(
        center_x+constants.inventory_window_width/2,
        constants.screen_center_y,
        constants.inventory_window_width - 2,
        height,
        arcade.color.WHITE_SMOKE
    )

    notice_window_title.draw()
    notice_window_content.draw()


def render_one_window(title_txt, content_txt, offset_x=0):
    global title
    global content

    center_x = constants.screen_center_x - constants.inventory_window_width/2
    center_x = int(center_x) + offset_x
    content_margin_left = 20
    if title is None:
        title = arcade.Text(
            "",
            center_x,
            (int(constants.screen_center_y
                 + constants.inventory_window_height/2)
             - constants.font_line_height*2),
            arcade.color.WHITE,  # type: ignore
            constants.font_size + 4,
            align='center',
            width=constants.inventory_window_width,
            font_name='LT Binary Neue Round',
        )
    if content is None:
        content = arcade.Text(
            "",
            center_x,
            int(constants.screen_center_y + constants.inventory_window_height /
                2) - constants.font_line_height*4,
            arcade.color.WHITE,  # type: ignore
            constants.font_size,
            multiline=True,
            align='left',
            width=constants.inventory_window_width,
            font_name='LT Binary Neue Round',
        )

    title.x = center_x
    content.x = center_x + content_margin_left
    title.text = title_txt
    content.text = content_txt

    arcade.draw_rectangle_filled(
        center_x+constants.inventory_window_width/2,
        constants.screen_center_y,
        constants.inventory_window_width,
        constants.inventory_window_height,
        arcade.color.BLACK_LEATHER_JACKET
    )
    arcade.draw_rectangle_outline(
        center_x+constants.inventory_window_width/2,
        constants.screen_center_y,
        constants.inventory_window_width - 2,
        constants.inventory_window_height,
        arcade.color.WHITE_SMOKE
    )

    title.draw()
    content.draw()


def render_one_auto_window(title_txt, content_txt, player_center_x):
    offset_x = constants.screen_width - constants.screen_center_x
    offset_x -= constants.inventory_window_width/2 + 10

    if player_center_x >= constants.screen_center_x:
        render_one_window(title_txt, content_txt, -offset_x)
    else:
        render_one_window(title_txt, content_txt, offset_x)


def render_tow_window(title_txt, content_txt, sub_title_txt, sub_content_txt):
    render_one_window(title_txt, content_txt,
                      constants.inventory_window_width/2 + 5)
    render_one_window(sub_title_txt, sub_content_txt,
                      -constants.inventory_window_width/2 - 5)
