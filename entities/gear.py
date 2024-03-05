
from entities.entity import Entity


class Gear(Entity):

    def __init__(
        self,
        *,
        entity_id: int = 0,
        x: int = 0,
        y: int = 0,
        name: str = "<Unnamed>",
        sprite_f=None,
    ):
        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            name=name,
            blocks_movement=False,
            sprite_f=sprite_f,
        )

    def to_dict(self):
        return dict(
            entity_id=self.entity_id,
            x=self.x,
            y=self.y,
        )

    def load_dict(self, d):
        self.x = d['x']
        self.y = d['y']
