class BaseComponent:
    entity = None

    @property
    def engine(self):
        return self.entity.gamemap.engine