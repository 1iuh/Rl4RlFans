import arcade

import tcod
from engine import Engine
from game_map import generate_dungeon
from charmap import charmap
import color
import entity_factories
import copy
import time
import traceback
from PIL import Image

# Constants

map_width = 50
map_height = 35
room_max_size = 10
room_min_size = 6
max_rooms = 30
max_monsters_per_room = 2
max_items_per_room = 5

screen_width = 24 * map_width
screen_height = 24 * map_height
screen_title = "Roguelike For Roguelike Fans"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(screen_width, screen_height, screen_title) # type: ignore

        arcade.set_background_color(arcade.csscolor.BLACK) # type: ignore

    def setup(self):
        self.player = copy.deepcopy(entity_factories.player)
        self.engine = Engine(player=self.player)
        self.engine.game_map = generate_dungeon(
            map_width,
            map_height,
            room_min_size,
            room_max_size,
            max_rooms,
            max_monsters_per_room,
            max_items_per_room,
            engine=self.engine,
            )
        self.engine.update_fov()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.engine.game_map.arcade_render()

    def on_update(self, delta_time):
        for entity in self.engine.game_map.entities:
            entity.sprite.update_animation(delta_time)

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed. """
        self.engine.event_handler.handle_events(symbol)

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
