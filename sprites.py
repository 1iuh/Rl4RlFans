from __future__ import annotations

import arcade
import math

from render_order import RenderOrder

from typing import TYPE_CHECKING
import sys
import os

if TYPE_CHECKING:
    from entities.entity import Missile


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


arcade.load_font(
        resource_path("asset/fonts/LTBinaryNeueRound-Regular.ttf"))

gear_textures = arcade.load_spritesheet(
    resource_path("asset/gears.png"), 48, 48, 16, 350, 0, None)
tileset_textures = arcade.load_spritesheet(
    resource_path("asset/Tiles and Walls 48x48.png"), 48, 48, 17, 153, 0, None)
big_zombie_textures = arcade.load_texture(
    resource_path("asset/frames/big_zombie_run_anim_f0.png"))
chort_textures = arcade.load_texture(resource_path(
    resource_path("asset/frames/chort_idle_anim_f0.png")))
background = arcade.load_texture(
    resource_path("asset/Background/background_0.png"))


class ItemSprite(arcade.Sprite):

    render_order: RenderOrder = RenderOrder.ITEM

    def __init__(self, path_or_texture, scale):
        super().__init__(path_or_texture, scale)


class ActorSprite(arcade.Sprite):

    corpse_texture = tileset_textures[99]
    is_alive = True
    render_order: RenderOrder = RenderOrder.ACTOR

    def __init__(self, filename: str, frame_number: int, scale: float):
        self.frames = []
        for i in range(frame_number):
            texture = arcade.load_texture(filename.format(i))
            keyframe = arcade.AnimationKeyframe(i, 100, texture)
            self.frames.append(keyframe)

        super().__init__(path_or_texture=self.frames[0].texture, scale=scale)
        self.cur_frame_idx = 0
        self.time_counter = 0.0

    def update_animation(self, delta_time: float = 1 / 60):
        if not self.is_alive:
            self.texture = self.corpse_texture
            self.scale = 0.5
            return
        self.time_counter += delta_time
        while self.time_counter > self.frames[self.cur_frame_idx].duration / 1000.0:
            self.time_counter -= self.frames[self.cur_frame_idx].duration / 1000.0
            self.cur_frame_idx += 1
            if self.cur_frame_idx >= len(self.frames):
                self.cur_frame_idx = 0

            self.texture = self.frames[self.cur_frame_idx].texture


class ConstructSprite(arcade.Sprite):

    def __init__(self, dark_texture: arcade.Texture,
                 light_texture: arcade.Texture, void_texture: arcade.Texture,
                 scale: float):

        super().__init__(scale=scale)
        self.is_seen = False
        self.dark_texture = dark_texture
        self.light_texture = light_texture
        self.void_texture = void_texture
        self.is_light = False
        self.update_texture()

    def set_is_seen(self, val):
        self.is_seen = val
        self.update_texture()

    def set_is_light(self, val):
        self.is_light = val
        self.update_texture()

    def update_texture(self):
        if not self.is_seen:
            self.texture = self.void_texture
        else:
            if self.is_light:
                self.texture = self.light_texture
            else:
                self.texture = self.dark_texture


class MissileSprite(arcade.Sprite):

    left_time: float = 0
    render_order: RenderOrder = RenderOrder.Missile
    entity: Missile

    def __init__(self, filename: str, frame_number: int, scale: float):
        self.frames = []
        for i in range(frame_number):
            texture = arcade.load_texture(filename.format(i))
            keyframe = arcade.AnimationKeyframe(i, 100, texture)
            self.frames.append(keyframe)

        super().__init__(path_or_texture=self.frames[0].texture, scale=scale)
        self.cur_frame_idx = 0
        self.time_counter = 0.0

    def set_duration(self, duration: float = 0.5):
        self.left_time = duration

    def set_target(self, x, y, target_x, target_y, duration: float = 0.5):
        velocity_x = target_x - x
        velocity_y = target_y - y

        self.angle = - math.degrees(math.atan2(velocity_y, velocity_x))

        self.velocity = velocity_x/duration, velocity_y / duration
        self.left_time = duration

    def on_update(self, delta_time: float = 1/60):
        if self.left_time <= 0:
            self.velocity = 0, 0
        else:
            self.position = (
                self._position[0] + self.change_x * delta_time,
                self._position[1] + self.change_y * delta_time,
            )
        self.left_time -= delta_time

    def update_animation(self, delta_time: float = 1 / 60):
        self.time_counter += delta_time
        while self.time_counter > self.frames[self.cur_frame_idx].duration / 1000.0:
            self.time_counter -= self.frames[self.cur_frame_idx].duration / 1000.0
            self.cur_frame_idx += 1
            if self.cur_frame_idx >= len(self.frames):
                self.cur_frame_idx = 0

            self.texture = self.frames[self.cur_frame_idx].texture


def floor_sprite_8():

    return ConstructSprite(
        tileset_textures[121],
        tileset_textures[120],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_7():

    return ConstructSprite(
        tileset_textures[104],
        tileset_textures[103],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_6():

    return ConstructSprite(
        tileset_textures[87],
        tileset_textures[86],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_5():

    return ConstructSprite(
        tileset_textures[70],
        tileset_textures[69],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_4():

    return ConstructSprite(
        tileset_textures[53],
        tileset_textures[52],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_3():

    return ConstructSprite(
        tileset_textures[36],
        tileset_textures[35],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_2():

    return ConstructSprite(
        tileset_textures[19],
        tileset_textures[18],
        tileset_textures[130],
        scale=0.5)


def floor_sprite_1():

    return ConstructSprite(
        tileset_textures[2],
        tileset_textures[1],
        tileset_textures[130],
        scale=0.5)


floor_sprites = [
        floor_sprite_1,
        floor_sprite_2,
        floor_sprite_3,
        floor_sprite_4,
        floor_sprite_5,
        floor_sprite_6,
        floor_sprite_7,
        floor_sprite_8,
        ]


def wall_sprite_5():
    return ConstructSprite(
        tileset_textures[78],
        tileset_textures[76],
        tileset_textures[130],
        scale=0.5)


def wall_sprite_4():
    return ConstructSprite(
        tileset_textures[44],
        tileset_textures[42],
        tileset_textures[130],
        scale=0.5)


def wall_sprite_3():
    return ConstructSprite(
        tileset_textures[47],
        tileset_textures[45],
        tileset_textures[130],
        scale=0.5)


def wall_sprite_1():
    return ConstructSprite(
        tileset_textures[13],
        tileset_textures[11],
        tileset_textures[130],
        scale=0.5)


def wall_sprite_2():
    return ConstructSprite(
        tileset_textures[125],
        tileset_textures[123],
        tileset_textures[130],
        scale=0.5)


wall_sprites = [
        wall_sprite_1,
        wall_sprite_2,
        wall_sprite_3,
        wall_sprite_4,
        wall_sprite_5,
        ]


def down_stair_sprite():
    return ConstructSprite(
        tileset_textures[83],
        tileset_textures[82],
        tileset_textures[130],
        scale=0.5)


def player_sprite():
    return ActorSprite(resource_path("asset/player_idle_f{0}.png"), 3, scale=1)


def Goblin_sprite():
    return ActorSprite(resource_path("asset/frames/goblin_idle_anim_f{0}.png"),
                       4, scale=1)


def Ice_zombie_sprite():
    return ActorSprite(resource_path("asset/frames/ice_zombie_anim_f{0}.png"),
                       4, scale=1)


def Imp_sprite():
    return ActorSprite(resource_path("asset/frames/imp_idle_anim_f{0}.png"),
                       4, scale=1)


def Masked_orc_sprite():
    return ActorSprite(
            resource_path("asset/frames/masked_orc_idle_anim_f{0}.png"),
            4, scale=1)


def Muddy_sprite():
    return ActorSprite(resource_path("asset/frames/muddy_anim_f{0}.png"),
                       4, scale=1)


def Necromancer_sprite():
    return ActorSprite(resource_path("asset/frames/necromancer_anim_f{0}.png"),
                       4, scale=1)


def Ogre_sprite():
    return ActorSprite(resource_path("asset/frames/ogre_idle_anim_f{0}.png"),
                       4, scale=0.8)


def Orc_shaman_sprite():
    return ActorSprite(
            resource_path("asset/frames/orc_shaman_idle_anim_f{0}.png"),
            4, scale=1)


def Orc_warrior_sprite():
    return ActorSprite(
            resource_path("asset/frames/orc_warrior_idle_anim_f{0}.png"),
            4, scale=1)


def Skelet_sprite():
    return ActorSprite(resource_path("asset/frames/skelet_idle_anim_f{0}.png"),
                       4, scale=1)


def Slug_sprite():
    return ActorSprite(resource_path("asset/frames/slug_anim_f{0}.png"),
                       4, scale=1)


def Swampy_sprite():
    return ActorSprite(resource_path("asset/frames/swampy_anim_f{0}.png"),
                       4, scale=1)


def Tiny_slug_sprite():
    return ActorSprite(resource_path("asset/frames/tiny_slug_anim_f{0}.png"),
                       4, scale=1)


def Tiny_zombie_sprite():
    return ActorSprite(
            resource_path("asset/frames/tiny_zombie_idle_anim_f{0}.png"),
            4, scale=1)


def Wogol_sprite():
    return ActorSprite(
            resource_path("asset/frames/wogol_idle_anim_f{0}.png"),
            4, scale=1)


def Zombie_sprite():
    return ActorSprite(resource_path("asset/frames/zombie_anim_f{0}.png"),
                       4, scale=1)


def Big_demon_sprite():
    return ActorSprite(
            resource_path("asset/frames/big_demon_idle_anim_f{0}.png"),
            4, scale=0.666)


def Big_zombie_sprite():
    return ActorSprite(
            resource_path("asset/frames/big_zombie_idle_anim_f{0}.png"),
            4, scale=0.666)


def Chort_sprite():
    return ActorSprite(
            resource_path("asset/frames/chort_idle_anim_f{0}.png"), 4, scale=1)


monster_sprites = [
    Goblin_sprite,
    Ice_zombie_sprite,
    Imp_sprite,
    Masked_orc_sprite,
    Muddy_sprite,
    Necromancer_sprite,
    Ogre_sprite,
    Orc_shaman_sprite,
    Orc_warrior_sprite,
    Skelet_sprite,
    Slug_sprite,
    Swampy_sprite,
    Tiny_slug_sprite,
    Tiny_zombie_sprite,
    Wogol_sprite,
    Zombie_sprite,
    Big_demon_sprite,
    Big_zombie_sprite,
    Chort_sprite
]


def Ma_po_tofu():
    return ActorSprite(
            resource_path("asset/frames/dwarf_m_idle_anim_f{0}.png"),
            4, scale=1)


def Feishiko():
    return ActorSprite(
            resource_path("asset/frames/lizard_m_idle_anim_f{0}.png"),
            4, scale=1)


def Silencess():
    return ActorSprite(
            resource_path("asset/frames/wizzard_m_idle_anim_f{0}.png"),
            4, scale=1)


def Super_light():
    return ActorSprite(
            resource_path("asset/frames/pumpkin_dude_idle_anim_f{0}.png"),
            4, scale=1)


def Sagancharum():
    return ActorSprite(
            resource_path("asset/frames/elf_f_idle_anim_f{0}.png"),
            4, scale=1)


def A_shu():
    return ActorSprite(
            resource_path("asset/frames/knight_f_idle_anim_f{0}.png"),
            4, scale=1)


def Twoflower():
    return ActorSprite(
            resource_path("asset/frames/doc_idle_anim_f{0}.png"),
            4, scale=1)


def Jade_Bird():
    return ActorSprite(
            resource_path("asset/frames/lizard_f_idle_anim_f{0}.png"),
            4, scale=1)


friends_sprites = [
        Ma_po_tofu,
        Feishiko,
        Silencess,
        Super_light,
        Sagancharum,
        A_shu,
        Twoflower,
        Jade_Bird,
        ]


def fireball_missile_sprite():
    return MissileSprite(resource_path("asset/fireball/1_{0}.png"), 20, 0.5)


def flame_sprite():
    return MissileSprite(
            resource_path("asset/FireVF/Fire+Sparks{0}.png"), 4, 0.4)


def lightning_sprite():
    return MissileSprite(resource_path("asset/lightning/f{0}.png"), 4, 0.2)


def sword_sprite():
    return ItemSprite(path_or_texture=gear_textures[336], scale=0.4)


def wand_sprite():
    return ItemSprite(path_or_texture=gear_textures[321], scale=0.4)


def hat():
    return ItemSprite(path_or_texture=gear_textures[176], scale=0.4)


def cloth():
    return ItemSprite(path_or_texture=gear_textures[0], scale=0.4)


def boot():
    return ItemSprite(path_or_texture=gear_textures[63], scale=0.4)


def iron_helmet_sprite():
    return ItemSprite(path_or_texture=gear_textures[187], scale=0.4)


def iron_armor_sprite():
    return ItemSprite(path_or_texture=gear_textures[1], scale=0.4)


def iron_boot_sprite():
    return ItemSprite(path_or_texture=gear_textures[64], scale=0.4)


def health_potion():
    return ItemSprite(path_or_texture=gear_textures[237], scale=0.4)


def mana_potion():
    return ItemSprite(path_or_texture=gear_textures[238], scale=0.4)
