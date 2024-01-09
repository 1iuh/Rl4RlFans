# Constants
map_width = 50
map_height = 35
room_max_size = 10
room_min_size = 6
max_rooms = 30
max_monsters_per_room = 5
max_items_per_room = 5

grid_size = 24

screen_width = grid_size * map_width + 5
screen_height = grid_size * map_height + 5

screen_title = "Roguelike For Roguelike Fans"

screen_center_x = screen_width / 2
screen_center_y = screen_height / 2
seconds_per_action = 0.2

font_size = 12
font_line_height = 16

history_viewer_width = screen_width - 600 
history_viewer_height = screen_height - 300
history_viewer_lines = 28

wall_tilecode = 1001
floor_tilecode = 1002

inventory_window_width = screen_width - 800 
inventory_window_height = screen_height - 600
