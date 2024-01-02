

import arcade

TILE_SCALING = 0.5

textures = arcade.load_spritesheet("./asset/Tiles and Walls 48x48.png", 48, 48, 17, 153, 0, None)

wall = arcade.Sprite(texture=textures[0], scale=TILE_SCALING)
floor = arcade.Sprite(texture=textures[1], scale=TILE_SCALING)
void = arcade.Sprite(texture=textures[100], scale=TILE_SCALING)
player = arcade.Sprite(texture=textures[2], scale=TILE_SCALING)
player1 = arcade.Sprite(texture=textures[3], scale=TILE_SCALING)
player2 = arcade.Sprite(texture=textures[4], scale=TILE_SCALING)
player3 = arcade.Sprite(texture=textures[5], scale=TILE_SCALING)
