
import numpy as np
import tcod
import color

class VisualEffect:

    def __init__(self, gamemap, char:str, sx, sy, dx, dy):
        self.char = char
        self.gamemap = gamemap
        self.sx = sx
        self.sy = sy
        self.dx = dx
        self.dy = dy
        self.path = self.get_path_to(dx, dy)
        self.isFinish = False

    def get_path_to(self, dest_x: int, dest_y: int):
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.sx, self.sy))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]

    def render(self, console):
        if len(self.path) == 0:
            self.on_path_end(console)
            return
        location = self.path.pop(0)
        console.print( x=location[0], y=location[1], string=self.char, fg=color.red)

    def on_path_end(self, console:tcod.Console):
        console.draw_frame(x=self.dx-1, y=self.dy-1, width=3, height=3, decoration=self.char * 9, fg=color.red)
        self.isFinish = True



        
