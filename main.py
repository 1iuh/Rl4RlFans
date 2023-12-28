#!/usr/bin/env python3
import tcod
from engine import Engine
from game_map import generate_dungeon
from charmap import charmap
import color
import entity_factories
import copy
import time
import traceback
import imageio.v2 as imageio


def main():
    screen_width = 50
    screen_height = 40
    map_width = 50
    map_height = 35
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2
    max_items_per_room = 5

    tileset = tcod.tileset.load_tilesheet(
        "asset/font24.png", 200, 92, charmap
    )
    tileset.set_tile(0x100000, imageio.imread("asset/floor.png"))
    tileset.set_tile(0x100001, imageio.imread("asset/wall.png"))
    tileset.set_tile(0x100002, imageio.imread("asset/idle0.png"))
    tileset.set_tile(0x100003, imageio.imread("asset/idle1.png"))
    tileset.set_tile(0x100004, imageio.imread("asset/idle2.png"))

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)
    engine.game_map = generate_dungeon(
        map_width,
        map_height,
        room_min_size,
        room_max_size,
        max_rooms,
        max_monsters_per_room,
        max_items_per_room,
        engine=engine,
        )

    engine.update_fov()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike For Roguelike Fans",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            if len(engine.game_map.visual_effects) > 0:
                time.sleep(0.1)
                continue
            try:
                for event in tcod.event.wait(0.1):
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)

 


if __name__ == "__main__":
    main()
