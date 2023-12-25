#!/usr/bin/env python3
import tcod
from engine import Engine
from game_map import generate_dungeon
from charmap import charmap
import entity_factories
import copy


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "asset/font2bitmap.png", 200, 92, charmap
    )

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)
    engine.game_map = generate_dungeon(
        map_width,
        map_height,
        room_min_size,
        room_max_size,
        max_rooms,
        max_monsters_per_room,
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
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
