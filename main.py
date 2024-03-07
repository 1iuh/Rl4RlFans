import arcade

from engine import GameEngine, StartMenuEngine
from game_map import generate_dungeon
from entities import actors
import copy
import constants

arcade.enable_timings()


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(
                constants.screen_width, constants.screen_height,
                constants.screen_title, update_rate=1/60,
                draw_rate=1/60)  # type: ignore
        arcade.set_background_color(arcade.csscolor.BLACK)  # type: ignore

    def setup(self):
        self.goto_start_menu()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.engine.on_render()
        # arcade.draw_text("%.2f" % arcade.get_fps(30), 100, 100)

    def on_update(self, delta_time):
        self.engine.on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        self.engine.on_key_press(symbol, modifiers)

    def goto_start_menu(self):
        self.engine = StartMenuEngine(self)
        self.engine.on_start()

    def continue_last_game(self):
        self.start_new_game()
        self.engine.continue_last_game()
        self.engine.on_start()

    def start_new_game(self):
        player = copy.deepcopy(actors.player)
        self.engine = GameEngine(player, self)
        self.engine.game_map = generate_dungeon(
            constants.map_width,
            constants.map_height,
            constants.room_min_size,
            constants.room_max_size,
            constants.max_rooms,
            constants.max_monsters_per_room,
            constants.max_items_per_room,
            1,
            engine=self.engine,
            )
        self.engine.on_start()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
