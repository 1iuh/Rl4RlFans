from __future__ import annotations

from typing import Callable, Optional, Tuple, TYPE_CHECKING
from arcade import key as arcade_key
import arcade
import constants

from actions import (
   Action,
   BumpAction,
   PickupAction,
   WaitAction
)
import actions
import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

MOVE_KEYS = {
    arcade_key.H: (-1, 0),
    arcade_key.J: (0, -1),
    arcade_key.K: (0, 1),
    arcade_key.L: (1, 0),
}

CURSOR_Y_KEYS = {
    arcade_key.UP: -1,
    arcade_key.DOWN: 1,
    arcade_key.PAGEUP: -10,
    arcade_key.PAGEDOWN: 10,
    arcade_key.J: -1,
    arcade_key.K: 1,
}

WAIT_KEYS = {
    arcade_key.PERIOD,
    arcade_key.KEY_5,
    arcade_key.CLEAR,
}

CONFIRM_KEYS = {
   arcade_key.RETURN,
}

class EventHandler:
    engine: Engine

    def __init__(self, engine):
        self.engine = engine

    def on_key_press(self, key):
        pass

    def handle_events(self, key) -> None:
        self.handle_action(self.on_key_press(key))

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        self.engine.render()
        return True

    def on_render(self) -> None:
        self.engine.render()



class MainGameEventHandler(EventHandler):

    def on_key_press(self, key):

        action: Optional[Action] = None

        player = self.engine.player

        if key in MOVE_KEYS:
            action = BumpAction(player, *MOVE_KEYS[key])
        elif key in WAIT_KEYS:
            action = WaitAction(self.engine)
        elif key == arcade_key.V:
            self.engine.event_handler = HistoryViewer(self.engine)
        elif key == arcade_key.G:
            action = PickupAction(player)
        elif key == arcade_key.I:
            self.engine.event_handler = InventoryActivateHandler(self.engine)
        elif key == arcade_key.D:
            self.engine.event_handler = InventoryDropHandler(self.engine)
        elif key == arcade_key.SLASH:
            self.engine.event_handler = LookHandler(self.engine)
        elif key == arcade_key.ESCAPE:
            raise SystemExit()

        # No valid key was pressed
        return action

class GameOverEventHandler(EventHandler):

    def on_key_press(self, key):
        if key == arcade_key.ESCAPE:
            raise SystemExit()


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length
        self.title = arcade.Text(
            "┤消息记录├",
            int(constants.screen_center_x - constants.history_viewer_width/2),
            int(constants.screen_center_y + constants.history_viewer_height/2) - 24,
            arcade.color.WHITE, # type: ignore
            constants.font_size,
            font_name='stsong',
            align='center',
            width=constants.history_viewer_width,
        )

    def on_render(self) -> None:
        super().on_render()  # Draw the main state as the background.

        # Draw a frame with a custom banner title.
        arcade.draw_rectangle_filled(
                constants.screen_center_x,
                constants.screen_center_y,
                constants.history_viewer_width,
                constants.history_viewer_height,
                arcade.color.BLACK_OLIVE
                )
        # Render the message log using the cursor parameter.
        self.title.draw()
        self.engine.message_log.render(
                int(constants.screen_center_x - constants.history_viewer_width/2) + 60,
                int(constants.screen_center_y + constants.history_viewer_height/2) - 60,
                lines=constants.history_viewer_lines,
                cursor=self.cursor
        )

    def on_key_press(self, key):
        # Fancy conditional movement to make it feel right.
        if key in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[key]
            if adjust < 0 and self.cursor <= constants.history_viewer_lines:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = constants.history_viewer_lines
            elif adjust > 0 and self.cursor == self.log_length:
                # Same with bottom to top movement.
                self.cursor = self.log_length
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length))
        else:  # Any other key moves back to the main game state.
            self.engine.event_handler = MainGameEventHandler(self.engine)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def handle_action(self, action: Optional[Action]) -> bool:
        """Return to the main event handler when a valid action was performed."""
        if super().handle_action(action):
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return True
        return False

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """By default any key exits this input handler."""
        if event.sym in {  # Ignore modifier keys.
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[Action]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        self.engine.event_handler = MainGameEventHandler(self.engine)
        return None


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)

        height = number_of_items_in_inventory + 2

        if height <= 3:
            height = 3

        if self.engine.player.x <= 20:
            x = 35
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)
                console.print(x + 1, y + i + 1, f"({item_key}) {item.name}")
        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "选择一个物品来使用"

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Return the action for the selected item."""
        return item.consumable.get_action(self.engine.player)


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "选择一个物品来摧毁"

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Drop this item."""
        return actions.DropItem(self.engine.player, item)


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y # type: ignore

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb["bg"][x, y] = color.white
        console.tiles_rgb["fg"][x, y] = color.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            # if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            #     modifier *= 5
            # if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
            #     modifier *= 10
            # if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
            #     modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y # type: ignore
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> None:
        """Return to main handler."""
        self.engine.event_handler = MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(
        self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]
    ):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
            self, engine: Engine, radius: int, callback: Callable[[Tuple[int, int]], Optional[Action]]
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius,
            y=y - self.radius,
            width=self.radius * 2 +1,
            height=self.radius * 2 +1,
            fg=color.red,
            clear=False,
        )
    

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))
