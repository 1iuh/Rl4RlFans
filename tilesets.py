import arcade

TILE_SCALING = 0.5
UPDATES_PER_FRAME = 5



class AnimationSprite(arcade.Sprite):

    def __init__(self, filename:str, frame_number, scale):
        self.frames = []
        for i in range(frame_number):
            texture = arcade.load_texture(filename.format(i))
            keyframe = arcade.AnimationKeyframe(i, 100, texture)
            self.frames.append(keyframe)

        super().__init__(path_or_texture=self.frames[0].texture, scale=scale)
        self.cur_frame_idx = 0
        self.time_counter = 0.0


    def update_animation(self, delta_time: float = 1 / 60):
        self.time_counter += delta_time
        while self.time_counter > self.frames[self.cur_frame_idx].duration / 1000.0:
            self.time_counter -= self.frames[self.cur_frame_idx].duration / 1000.0
            self.cur_frame_idx += 1
            if self.cur_frame_idx >= len(self.frames):
                self.cur_frame_idx = 0

            self.texture = self.frames[self.cur_frame_idx].texture

tileset_textures = arcade.load_spritesheet("./asset/Tiles and Walls 48x48.png", 48, 48, 17, 153, 0, None)
potions_textures = arcade.load_spritesheet("./asset/Potions 48x48.png", 48, 48, 5, 50, 0, None)
big_zombie_textures = arcade.load_texture("./asset/frames/big_zombie_run_anim_f0.png")
chort_textures = arcade.load_texture("./asset/frames/chort_idle_anim_f0.png")


wall_light = arcade.Sprite(path_or_texture=tileset_textures[2], scale=TILE_SCALING)
wall_dark = arcade.Sprite(path_or_texture=tileset_textures[1], scale=TILE_SCALING)
floor_light = arcade.Sprite(path_or_texture=tileset_textures[12], scale=TILE_SCALING)
floor_dark = arcade.Sprite(path_or_texture=tileset_textures[11], scale=TILE_SCALING)
void = arcade.Sprite(path_or_texture=tileset_textures[100], scale=TILE_SCALING)


player = AnimationSprite("./asset/player_idle_f{0}.png", 3, scale=1)
big_demon = AnimationSprite("./asset/frames/big_demon_idle_anim_f{0}.png", 4, scale=0.666)
big_zombie = AnimationSprite("./asset/frames/big_zombie_idle_anim_f{0}.png", 4, scale=0.666)
chort = AnimationSprite("./asset/frames/chort_idle_anim_f{0}.png", 4, scale=1)
toufu = AnimationSprite("./asset/frames/dwarf_m_idle_anim_f{0}.png", 4, scale=1)
feishiko = AnimationSprite("./asset/frames/lizard_m_idle_anim_f{0}.png", 4, scale=1)
silencess = AnimationSprite("./asset/frames/wizzard_m_idle_anim_f{0}.png", 4, scale=1)
superlight = AnimationSprite("./asset/frames/pumpkin_dude_idle_anim_f{0}.png", 4, scale=1)

potion_0 = arcade.Sprite(path_or_texture=potions_textures[0], scale=0.4)
potion_1 = arcade.Sprite(path_or_texture=potions_textures[10], scale=0.4)
potion_2 = arcade.Sprite(path_or_texture=potions_textures[20], scale=0.4)
potion_3 = arcade.Sprite(path_or_texture=potions_textures[30], scale=0.4)
