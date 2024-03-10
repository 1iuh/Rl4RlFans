from entities.entity import VisualEffects, Missile
from components import ai
import sprites


fireVFX = VisualEffects(
                    9000,
                    sprite_f=sprites.flame_sprite,
                    ai_cls=ai.VfxAI,
                    actor=None
                )

lightning_fx = VisualEffects(
                    9002,
                    sprite_f=sprites.lightning_sprite,
                    ai_cls=ai.VfxAI,
                    actor=None
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
            ai_cls=ai.MissileAI,
        )
