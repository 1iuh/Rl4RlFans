class Skill:
    name = "Unnamed"
    consumable = None
    mana_cost = 1
    parent = None
    desc = "skill desc"

    @property
    def gamemap(self):
        return self.parent.parent

    def __init__(self, name, desc, mana_cost, consumable, parent):
        self.name = name
        self.desc = desc
        self.consumable = consumable
        self.consumable.parent = self
        self.mana_cost = mana_cost
        self.parent = parent
