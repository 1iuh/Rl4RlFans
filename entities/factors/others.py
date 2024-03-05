from entities.entity import VisualEffects, Missile
from components.ai import MissileAI, VfxAI
import sprites


fireVFX = VisualEffects(
                    9000,
                    x=0,
                    y=0,
                    sprite_f=sprites.flame_sprite,
                    ai_cls=VfxAI
                )

fireball_missile = Missile(
            entity_id=9001,
            x=0,
            y=0,
            target_xy=(0, 0),
            sprite_f=sprites.fireball_missile_sprite,
            damage=0,
            radius=0,
            parent=None,
            ai_cls=MissileAI,
        )

if __name__ == '__main__':
    fireVFX.copy()
