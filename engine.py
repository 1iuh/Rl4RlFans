from __future__ import annotations

from tcod.map import compute_fov
from input_handlers import (MainGameEventHandler, StartMenuEventHandler,
                            WinEventHandler, HotKeysEventHandler, ResetWorldEventHandler)
from message_log import MessageLog
from entities.actor import Actor
from render_functions import render_bar, render_mob_bar
import constants
import arcade
import json
import sprites
import env_val


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap
    from input_handlers import EventHandler
    from actions import Action
    from main import MyGame


class Engine:

    window: MyGame

    def __init__(self, window):
        self.window = window

    def on_start(self):
        raise NotImplementedError

    def on_render(self):
        raise NotImplementedError

    def on_update(self, delta_time):
        raise NotImplementedError

    def on_key_press(self, symbol, modifiers):
        raise NotImplementedError


class StartMenuEngine(Engine):

    cursor_index: int = 0
    window: MyGame
    title = 'A Roguelike\nFor\nRoguelike Fans'
    options = [
        'Start Game',
        'Reset World',
        'Exit',
    ]

    def __init__(self, window):
        self.window = window
        self.event_handler = StartMenuEventHandler(self)

    def on_start(self):
        self.background = sprites.background

    def on_render(self):
        # draw background
        arcade.draw_lrwh_rectangle_textured(
            200, 50,
            constants.screen_width - 400, constants.screen_height - 100,
            self.background
        )
        # draw tile
        arcade.draw_text(
            self.title,
            constants.screen_center_x-350, 600, arcade.color.WHITE, 36,
            font_name=constants.font_name,
            width=500,
            multiline=True,
            align='center'
        )

        # draw options
        self.cursor_index %= len(self.options)
        i = 0
        for option in self.options:
            if i == self.cursor_index:
                option = f"=> {option} <="
            arcade.draw_text(
                option,
                int(constants.screen_center_x) - 100,
                int(constants.screen_center_y - 50 - 26*i),
                arcade.color.WHITE, 22, anchor_x='center',
                font_name=constants.font_name
            )
            i += 1
        self.event_handler.on_render()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol, modifiers):
        self.event_handler.on_key_press(symbol, modifiers)

    def excute_option(self):
        if self.cursor_index == 0:
            self.window.start_new_game()
        if self.cursor_index == 1:
            self.reset_world()
        elif self.cursor_index == 2:
            arcade.exit()

    def reset_world(self):
        save_data = json.dumps(dict())
        with open(sprites.resource_path('asset/savegame.sav'), "wb") as f:
            f.write(save_data.encode("utf8"))
        self.event_handler = ResetWorldEventHandler(self)


class GameEngine(Engine):

    event_handler: EventHandler
    game_map: GameMap

    def __init__(self, player: Actor, window):

        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

        self.player = player
        self.action_queue: list[Action] = []
        super().__init__(window)

    def on_start(self):

        if (self.game_map.level == 1):
            self.event_handler: EventHandler = HotKeysEventHandler(self)
        else:
            self.event_handler: EventHandler = MainGameEventHandler(self)

        self.load()
        self.update_fov()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""

        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def update_camera(self):
        self.window.camera.center(self.player.sprite.position)
        self.window.camera.use()

    def on_update(self, delta_time):
        self.event_handler.on_update(delta_time)

    def on_render(self):
        self.event_handler.on_render()

    def on_key_press(self, symbol, modifiers):
        self.event_handler.handle_events(symbol, modifiers)

    def render(self) -> None:
        self.game_map.render()
        self.render_ui()

    def render_ui(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            190,
            0,
            constants.screen_height,
            arcade.color.BLACK_LEATHER_JACKET
        )
        arcade.draw_lrbt_rectangle_outline(
            0,
            190,
            0,
            constants.screen_height,
            arcade.color.WHITE_SMOKE
        )
        self.message_log.render(x=10, y=410, lines=14)
        i = 0
        render_bar(
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=12,
            color=arcade.color.RED_ORANGE,
            start_y=800 - 24 * i,
            name='HP'
        )
        i += 1
        render_bar(
            current_value=self.player.fighter.mp,
            maximum_value=self.player.fighter.max_mp,
            total_width=12,
            color=arcade.color.BABY_BLUE,
            start_y=800 - 24 * i,
            name='MP'
        )

        i = 1
        stats_start_x = 30
        font_line_height = 18

        arcade.draw_text(
            f'Dungeon depth: {self.game_map.level}',
            stats_start_x - 12,
            constants.screen_height - 100 - font_line_height * i,
            font_size=14,
            font_name=constants.font_name
        )
        i += 2
        arcade.draw_text(
            'Stats:',
            stats_start_x - 12,
            constants.screen_height - 100 - font_line_height * i,
            font_size=14,
            font_name=constants.font_name
        )
        i += 1
        arcade.draw_text(
            f'Power: {self.player.fighter.power}',
            stats_start_x,
            constants.screen_height - 100 - font_line_height * i,
            font_name=constants.font_name
        )
        i += 1
        arcade.draw_text(
            f'Defense: {self.player.fighter.defense}',
            stats_start_x,
            constants.screen_height - 100 - font_line_height * i,
            font_name=constants.font_name
        )
        i += 1
        arcade.draw_text(
            f'Speed: {self.player.fighter.speed}',
            stats_start_x,
            constants.screen_height - 100 - font_line_height * i,
            font_name=constants.font_name
        )
        i += 1
        arcade.draw_text(
            f'Magic: {self.player.fighter.magic}',
            stats_start_x,
            constants.screen_height - 100 - font_line_height * i,
            font_name=constants.font_name
        )

        i += 2
        arcade.draw_text(
            'Equipments:',
            stats_start_x - 10,
            constants.screen_height - 100 - font_line_height * i,
            font_size=14,
            font_name=constants.font_name
        )
        i += 1

        for d in self.player.equipment.gears:
            key = d[0]
            val = d[1]
            if val is None:
                gear_name = 'null'
            else:
                gear_name = val.name
            arcade.draw_text(
                f'{key}:',
                stats_start_x,
                constants.screen_height - 100 - font_line_height * i,
                font_name=constants.font_name
            )
            i += 1
            arcade.draw_text(
                f'└ {gear_name}',
                stats_start_x,
                constants.screen_height - 100 - font_line_height * i,
                font_size=10,
                font_name=constants.font_name
            )
            i += 1

        i += 1
        arcade.draw_text(
            'Press ? For help',
            stats_start_x - 10,
            constants.screen_height - 100 - font_line_height * i,
            font_size=12,
            font_name=constants.font_name
        )
        i += 1

        for entity in self.game_map.entities:
            if entity.sprite.visible and isinstance(entity, Actor) and entity.is_monster():
                current_value = entity.fighter.hp
                maximum_value = entity.fighter.max_hp
                render_mob_bar(current_value, maximum_value,
                               entity.sprite.center_x,
                               entity.sprite.center_y)

        

    # def continue_last_game(self):
        # with open(sprites.resource_path('assets/savegame.sav'), "r") as f:
            # game_data = json.loads(f.read())
            # self.game_map.load_dict(game_data['game_map'])
            # self.player.load_dict(game_data['player'])
            # self.game_map.spawn_entity(self.player)

    def quit(self):
        self.window.goto_start_menu()

    def load(self):
        with open(sprites.resource_path('asset/savegame.sav'), "r") as f:
            game_data = json.loads(f.read())
            env_val.load_dict(game_data)

    def save(self):
        save_data = json.dumps(env_val.dict_dump())
        with open(sprites.resource_path('asset/savegame.sav'), "wb") as f:
            f.write(save_data.encode("utf8"))

    # def save_and_quit(self):
        # save_data = json.dumps(self.to_dict())
        # with open('./saves/savegame.sav', "wb") as f:
            # f.write(save_data.encode("utf8"))
        # self.window.goto_start_menu()

    def enter_next_level(self):
        if (self.game_map.tiles[self.player.x, self.player.y][2] ==
                constants.down_stair_tilecode):
            if (self.game_map.level >= env_val.end_level):
                self.event_handler = WinEventHandler(self)
            else:
                self.window.enter_next_level()

    def to_dict(self) -> dict:
        return dict(
            player=self.player.to_dict(),
            game_map=self.game_map.to_dict()
        )
