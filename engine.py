from __future__ import annotations

from tcod.map import compute_fov
from input_handlers import MainGameEventHandler, StartMenuEventHandler
from message_log import MessageLog
from render_functions import render_bar
import constants
import arcade
import json


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Actor
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
    title = 'Roguelike For Roguelike Fans'
    options = [
        'New Game',
        'Continue',
        'Config',
        'Exit',
    ]

    def __init__(self, window):
        self.window = window
        self.event_handler = StartMenuEventHandler(self)

    def on_start(self):
        self.background = arcade.load_texture(
            "./asset/Background/background_0.png")

    def on_render(self):
        # draw background
        arcade.draw_lrwh_rectangle_textured(
            200, 50,
            constants.screen_width - 400, constants.screen_height - 100,
            self.background
        )
        # draw tile
        arcade.draw_text(
            self.title, 150, 500, arcade.color.WHITE, 36,
            font_name="Kenney Blocks"
        )

        # draw options
        self.cursor_index %= len(self.options)
        i = 0
        for option in self.options:
            if i == self.cursor_index:
                option = f"=> {option} <="
            arcade.draw_text(
                option,
                int(constants.screen_center_x),
                int(constants.screen_center_y - 50 - 26*i),
                arcade.color.WHITE, 22, anchor_x='center'
            )
            i += 1

    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol, modifiers):
        self.event_handler.on_key_press(symbol, modifiers)

    def excute_option(self):
        if self.cursor_index == 0:
            self.window.start_new_game()
        elif self.cursor_index == 1:
            self.window.continue_last_game()
        elif self.cursor_index == 3:
            arcade.exit()


class GameEngine(Engine):

    game_map: GameMap

    def __init__(self, player: Actor, window):

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

        self.player = player
        self.action_queue: list[Action] = []
        super().__init__(window)

    def on_start(self):
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
        # self.window.camera.center(self.player.sprite.position)
        # self.window.camera.use()
        pass

    def on_update(self, delta_time):
        self.event_handler.on_update(delta_time)

    def on_render(self):
        self.event_handler.on_render()

    def on_key_press(self, symbol, modifiers):
        self.event_handler.handle_events(symbol, modifiers)

    def render(self) -> None:
        self.game_map.render()
        self.message_log.render(x=14, y=720, lines=10)
        render_bar(
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=12,
        )
        arcade.draw_text(f'Power: {self.player.fighter.power}',
                         10,
                         constants.screen_height-20
                         )
        arcade.draw_text(f'Defense: {self.player.fighter.defense}',
                         10,
                         constants.screen_height-40
                         )
        arcade.draw_text(f'Speed: {self.player.fighter.speed}',
                         10,
                         constants.screen_height-60
                         )
        arcade.draw_text(f'Magic: {self.player.fighter.magic}',
                         10,
                         constants.screen_height-80
                         )
        arcade.draw_text(f'Mp: {self.player.fighter.mp}',
                         10,
                         constants.screen_height-100
                         )

    def continue_last_game(self):
        with open('./saves/savegame.sav', "r") as f:
            game_data = json.loads(f.read())
            self.game_map.load_dict(game_data['game_map'])
            self.player.load_dict(game_data['player'])
            self.game_map.spawn_entity(self.player)

    def save_and_quit(self):
        save_data = json.dumps(self.to_dict())
        with open('./saves/savegame.sav', "wb") as f:
            f.write(save_data.encode("utf8"))
        self.window.goto_start_menu()

    def to_dict(self) -> dict:
        return dict(
                player=self.player.to_dict(),
                game_map=self.game_map.to_dict()
        )
