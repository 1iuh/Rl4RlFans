# Constants
map_width = 50
map_height = 35
room_max_size = 10
room_min_size = 6
max_rooms = 30

grid_size = 24

screen_width = grid_size * map_width + 5
screen_height = grid_size * map_height + 5

screen_title = "Roguelike For Roguelike Fans"

screen_center_x = int(screen_width / 2) + 100
screen_center_y = int(screen_height / 2)
seconds_per_action = 0.05

font_size = 12
font_line_height = 16

history_viewer_width = screen_width - 600
history_viewer_height = screen_height - 300
history_viewer_lines = 28

wall_tilecode = 1001
floor_tilecode = 1002
down_stair_tilecode = 1003

inventory_window_width = screen_width - 800
inventory_window_height = screen_height - 300

font_name = 'LT Binary Neue Round'
sub_line_placeholder = '       └ '

missile_move_speed = 4
end_level = 6

actor_stats_keys = [
    'power',
    'max_hp',
    'magic',
    'defense',
    'max_mp',
    'speed',
]


class MonsterType:
    Minion = 1
    Ranger = 2
    Tank = 3
    Assassin = 4


max_monsters_per_room = 2
max_items_per_room = 2
item_generate_rate = 0.25
gear_generate_rate = 0.15
monster_drop_rate = 0.4
enchant_bonus = 1
enchant_stats_bonus = 1
gear_base_stat_bonus = 1
monster_stat_bonus = 1
