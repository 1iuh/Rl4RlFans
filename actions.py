class Action:
    def __init__(self, entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
   def __init__(self, entity, dx, dy):
       super().__init__(entity)

       self.dx = dx
       self.dy = dy

   @property
   def dest_xy(self):
       """Returns this actions destination."""
       return self.entity.x + self.dx, self.entity.y + self.dy

   @property
   def blocking_entity(self):
       """Return the blocking entity at this actions destination.."""
       return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

   def perform(self) -> None:
      raise NotImplementedError()


class MeleeAction(ActionWithDirection):

   def perform(self) -> None:
       target = self.blocking_entity
       if not target:
           return  # No entity to attack.

       print(f"You kick the {target.name}, much to its annoyance!")


class MovementAction(ActionWithDirection):

    def perform(self):
        dest_x, dest_y = self.dest_xy
        

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):

            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)


class WaitAction(Action):
   def perform(self):
       pass


class BumpAction(ActionWithDirection):

   def perform(self):
    if self.blocking_entity:
        return MeleeAction(self.entity, self.dx, self.dy).perform()
    else:
        return MovementAction(self.entity, self.dx, self.dy).perform()