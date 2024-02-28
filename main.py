import arcade

from engine import Engine
from game_map import generate_dungeon
import entity_factories
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
        self.engine.on_start()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.engine.event_handler.on_render()
        arcade.draw_text("%.2f" % arcade.get_fps(30), 100, 100)

    def on_update(self, delta_time):

        self.engine.event_handler.on_update(delta_time)
        #  self.engine.game_map.missile_sprites.on_update(delta_time)
        #  for entity in self.engine.game_map.entities:
            #  entity.sprite.update_animation(delta_time)
        #  for entity in self.engine.game_map.missiles:
            #  entity.on_update()

    def on_key_press(self, symbol, modifiers):
        if len(self.engine.action_queue) > 0:
            return
        """Called whenever a key is pressed. """
        self.engine.event_handler.handle_events(symbol, modifiers)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
