import arcade

from engine import Engine
from game_map import generate_dungeon
import entity_factories
import copy
import time
import traceback
import constants

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(constants.screen_width, constants.screen_height, constants.screen_title) # type: ignore

        arcade.set_background_color(arcade.csscolor.BLACK) # type: ignore

    def setup(self):
        self.player = copy.deepcopy(entity_factories.player)
        self.engine = Engine(player=self.player)
        self.engine.game_map = generate_dungeon(
            constants.map_width,
            constants.map_height,
            constants.room_min_size,
            constants.room_max_size,
            constants.max_rooms,
            constants.max_monsters_per_room,
            constants.max_items_per_room,
            engine=self.engine,
            )
        self.engine.update_fov()
        # arcade.load_font('./asset/stsong.ttf')

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.engine.event_handler.on_render()
        self.time_now = time.time()
        if self.time_now - time.time() > 0.1:
            print("lagggggggggggggggg")

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
