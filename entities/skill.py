class Skill:
    name = "Unnamed"
    consumable = None
    mana_cost = 1
    parent = None

    @property
    def gamemap(self):
        return self.parent.parent

    def __init__(self, name, mana_cost, consumable, parent):
        self.name = name
        self.consumable = consumable
        self.consumable.parent = self
        self.mana_cost = mana_cost
        self.parent = parent
