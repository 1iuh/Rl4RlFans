from __future__ import annotations

from arcade import key as arcade_key
from render_functions import (render_one_window, render_tow_window,
                              render_one_auto_window, render_notice_window)
import arcade
import constants
import math

from actions import (
    Action,
    BumpAction,
    PickupAction,
    WaitAction
)
import actions
import color
import exceptions

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from engine import GameEngine, StartMenuEngine
    from entities.entity import Item
    from entities.gear import Gear

MOVE_KEYS = {
    arcade_key.H: (-1, 0),
    arcade_key.LEFT:  (-1, 0),
    arcade_key.J: (0, -1),
    arcade_key.DOWN: (0, -1),
    arcade_key.K: (0, 1),
    arcade_key.UP: (0, 1),
    arcade_key.L: (1, 0),
    arcade_key.RIGHT:  (1, 0),
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
    delta_time = 0.0
    engine: GameEngine

    def __init__(self, engine):
        self.engine = engine

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        pass

    def handle_events(self, key, modifiers) -> None:
        try:
            self.handle_action(self.on_key_press(key, modifiers))
        except exceptions.PlayerDie:
            death_message = "You die."
            death_message_color = color.player_die
            self.engine.message_log.add_message(
                    death_message, death_message_color)
            self.engine.event_handler = GameOverEventHandler(self.engine)

    def handle_action(self, action: Optional[Action]) -> bool:
        pass

    def on_update(self, delta_time):
        pass

    def on_render(self) -> None:
        self.engine.render()


class MainGameEventHandler(EventHandler):

    def handle_enemy_turns(self, player_action) -> None:
        self.engine.message_log.add_message("== New Turn ==")
        action_queue = [player_action]
        for entity in set(
                self.engine.game_map.entities) - {self.engine.player}:
            if not hasattr(entity, 'ai'):
                continue
            if entity.ai:
                try:
                    action_queue.append(entity.ai.perform())
                except exceptions.Impossible as exc:
                    self.engine.message_log.add_message(
                            exc.args[0], color.impossible)
        action_queue.sort(key=lambda x: x.speed, reverse=True)
        for act in action_queue:
            if hasattr(act.entity, 'is_alive') and not act.entity.is_alive:
                continue
            act.perform()
        self.engine.update_fov()

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        self.handle_enemy_turns(action)
        return True

    def on_update(self, delta_time):
        self.delta_time += delta_time
        for entity in self.engine.game_map.entities:
            entity.sprite.update_animation(delta_time)

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        action: Optional[Action] = None
        player = self.engine.player

        if key in MOVE_KEYS:
            action = BumpAction(player, *MOVE_KEYS[key])
        elif key == arcade_key.ENTER:
            self.engine.enter_next_level()
        elif key in WAIT_KEYS:
            action = WaitAction(self.engine)
        elif key == arcade_key.V:
            self.engine.event_handler = HistoryViewer(self.engine)
        elif key == arcade_key.G:
            action = PickupAction(player)
        elif key == arcade_key.I:
            self.engine.event_handler = InventoryActivateHandler(self.engine)
        elif key == arcade_key.E:
            self.engine.event_handler = EquipmentEventHandler(self.engine)
        elif key == arcade_key.D:
            self.engine.event_handler = InventoryDropHandler(self.engine)
        elif key == arcade_key.S:
            self.engine.event_handler = SkillHandler(self.engine)
        elif key == arcade_key.SPACE:
            self.engine.event_handler = LookHandler(self.engine)
        elif key == arcade_key.ESCAPE:
            self.engine.event_handler = EscMenuHandler(self.engine)

        # No valid key was pressed
        return action


class GameOverEventHandler(EventHandler):

    TITLE = "You Die."

    def __init__(self, engine):
        super().__init__(engine)

    def on_render(self) -> None:
        super().on_render()  # Draw the main state as the background.
        render_notice_window(self.TITLE, "Press Esc to continue.")

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        if key == arcade_key.ESCAPE:
            return self.engine.quit()


class WinEventHandler(EventHandler):

    TITLE = "You Win."

    def __init__(self, engine):
        super().__init__(engine)

    def on_render(self) -> None:
        super().on_render()  # Draw the main state as the background.
        render_notice_window(self.TITLE, "Press Esc to continue.")

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        if key == arcade_key.ESCAPE:
            return self.engine.quit()


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length
        self.title = arcade.Text(
            "┤Message History├",
            int(constants.screen_center_x - constants.history_viewer_width/2),
            (int(constants.screen_center_y + constants.history_viewer_height/2)
                - 24),
            arcade.color.WHITE,  # type: ignore
            constants.font_size,
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
            int(constants.screen_center_x -
                constants.history_viewer_width/2) + 60,
            int(constants.screen_center_y +
                constants.history_viewer_height/2) - 60,
            lines=constants.history_viewer_lines,
            cursor=self.cursor
        )

    def on_key_press(self, key, modifiers) -> Optional[Action]:
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
                # Otherwise move while staying clamped
                # to the bounds of the history log.
                self.cursor = max(
                    0, min(self.cursor + adjust, self.log_length))
        else:  # Any other key moves back to the main game state.
            self.engine.event_handler = MainGameEventHandler(self.engine)


class AskUserEventHandler(MainGameEventHandler):
    """Handles user input for actions which require special input."""

    def handle_action(self, action: Optional[Action]) -> bool:
        # Return to the main event handler when a valid action was performed.
        if super().handle_action(action):
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return True
        return False

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        """By default any key exits this input handler."""
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

    def on_render(self) -> None:
        super().on_render()

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        player = self.engine.player
        index = key - arcade_key.A

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message(
                    "Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().on_key_press(key, modifiers)

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class SkillHandler(InventoryEventHandler):

    TITLE = "Skills"

    def on_render(self) -> None:
        super().on_render()
        number_of_items = len(self.engine.player.skills)

        content = ''
        if number_of_items > 0:
            for i, item in enumerate(self.engine.player.skills):
                item_key = chr(ord("a") + i)
                content += f'({item_key}) {item.name}\n'
                content += f'    └ cost: {item.mana_cost},'
                content += f' damage: {item.desc}\n'
        else:
            content = '(null)'

        render_one_window(self.TITLE, content)

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        player = self.engine.player
        index = key - arcade_key.A

        if 0 <= index <= 26:
            try:
                selected_item = player.skills[index]
            except IndexError:
                self.engine.message_log.add_message(
                    "Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().on_key_press(key, modifiers)

    def on_item_selected(self, skill) -> Optional[Action]:
        """Called when the user selects a valid item."""
        if self.engine.player.fighter.mp < skill.mana_cost:
            self.engine.message_log.add_message(
                "Mana Not Enough.", color.invalid)
            return None
        else:
            return skill.consumable.get_action(self.engine.player)


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Inventory"
    sub_title = "Equipment"

    def __init__(self, engine):
        super().__init__(engine)

    def on_render(self) -> None:
        super().on_render()

        number_of_items_in_inventory = len(self.engine.player.inventory.items)
        content = ''
        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)
                content += f'({item_key}) {item.name}\n'
                content += f'        └ {item.attributes}\n'
        else:
            content = '(empty)'

        sub_content = ''
        for i, t in enumerate(self.engine.player.equipment.gears):
            key = t[0]
            val = t[1]
            if val is None:
                sub_content += f'{key}: null\n'
            else:
                sub_content += f'{key}: {val.name}\n'
                sub_content += f'    └ {val.attributes}\n'
        render_tow_window(self.TITLE, content, self.sub_title, sub_content)

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Return the action for the selected item."""
        return item.consumable.get_action(self.engine.player)


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select a item to drop."

    def on_render(self) -> None:
        super().on_render()

        number_of_items_in_inventory = len(self.engine.player.inventory.items)
        content = ''
        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)
                content += f'({item_key}) {item.name}\n'
                content += f'        └ {item.attributes}\n'
        else:
            content = '(empty)'

        render_one_window(self.TITLE, content)

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Drop this item."""
        return actions.DropItem(self.engine.player, item)


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: GameEngine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y  # type: ignore

    def on_render(self) -> None:
        """Highlight the tile under the cursor."""
        super().on_render()
        x, y = self.engine.mouse_location
        arcade.draw_rectangle_filled(
            x*constants.grid_size,
            y*constants.grid_size,
            constants.grid_size,
            constants.grid_size,
            color.white_transparent
        )

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        """Check for key movement or confirmation keys."""
        if key in MOVE_KEYS:
            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx
            y += dy
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y  # type: ignore
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().on_key_press(key, modifiers)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(AskUserEventHandler):
    TITLE = 'Monsters And Items'

    def __init__(self, engine):
        super().__init__(engine)

        self.x_offset = 300
        if self.engine.player.x >= constants.map_width/2:
            self.x_offset = -self.x_offset

    def on_render(self) -> None:
        super().on_render()

        content = ''
        for i, actor in enumerate(self.engine.game_map.visible_monsters):
            item_key = chr(ord("a") + i)
            content += f'({item_key}) {actor.name} '
            if actor.is_alive:
                content += f'  hp: {actor.fighter.hp}'
                content += f'  ack: {actor.fighter.power}'
                content += f'  def: {actor.fighter.defense}'
                content += f'  spd: {actor.fighter.speed}'
            content += '\n'
            arcade.draw_text(item_key,
                             actor.sprite.center_x,
                             actor.sprite.center_y,
                             anchor_x='center',
                             anchor_y='center',
                             )

        content += "\n"
        for i, item in enumerate(self.engine.game_map.visible_items):
            item_key = chr(ord("A") + i)
            content += f'({item_key}) {item.name}\n'
            arcade.draw_text(item_key,
                             item.sprite.center_x,
                             item.sprite.center_y,
                             anchor_x='center',
                             anchor_y='center',
                             )
        render_one_auto_window(self.TITLE, content,
                               self.engine.player.sprite.center_x)

    def on_index_selected(self, x: int, y: int) -> None:
        """Return to main handler."""
        self.engine.event_handler = MainGameEventHandler(self.engine)


class EscMenuHandler(AskUserEventHandler):
    options = ['Resume', 'Quit']
    cursor_index = 0

    def __init__(self, engine: GameEngine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)

    def on_render(self) -> None:
        """Highlight the tile under the cursor."""
        super().on_render()
        arcade.draw_lrbt_rectangle_filled(
            0,
            constants.screen_width,
            0,
            constants.screen_height,
            color.black_transparent
        )
        self.cursor_index %= len(self.options)
        i = 0
        for option in self.options:
            if i == self.cursor_index:
                option = f'=> {option} <='
            arcade.draw_text(
                option,
                constants.screen_center_x,
                constants.screen_center_y - i * 28,
                anchor_x='center',
                font_size=24
            )
            i += 1

    def on_key_press(self, key, modifiers):
        if key in (arcade_key.K, arcade_key.UP):
            self.cursor_index -= 1
        elif key in (arcade_key.J, arcade_key.DOWN):
            self.cursor_index += 1
        elif key in CONFIRM_KEYS:
            return self.on_index_selected()
        else:
            self.cursor_index = 0
            return self.on_index_selected()

    def on_index_selected(self) -> None:
        """Return to main handler."""
        if self.cursor_index == 1:
            self.engine.quit()
        else:
            self.engine.event_handler = MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy.
    Only the enemy selected will be affected.
    """

    def __init__(self, engine: GameEngine, callback):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius.
    Any entity within the area will be affected.
    """

    def __init__(
            self, engine: GameEngine, radius: int, callback
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self) -> None:
        """Highlight the tile under the cursor."""
        super().on_render()

        x, y = self.engine.mouse_location

        for _ in range(self.radius):
            for _x in range(x-self.radius, x + self.radius+1):
                for _y in range(y-self.radius, y + self.radius+1):
                    if (self.distance(x, y, _x, _y) > self.radius):
                        continue
                    arcade.draw_rectangle_filled(
                        _x*constants.grid_size,
                        _y*constants.grid_size,
                        constants.grid_size,
                        constants.grid_size,
                        color.white_transparent
                    )

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))

    def distance(self, x: int, y: int, _x: int, _y: int) -> float:
        return math.sqrt((x - _x) ** 2 + (y - _y) ** 2)


class StartMenuEventHandler:
    engine: StartMenuEngine

    def __init__(self, engine):
        self.engine = engine

    def on_key_press(self, key, modifiers):
        if key in (arcade_key.K, arcade_key.UP):
            self.engine.cursor_index -= 1
        elif key in (arcade_key.J, arcade_key.DOWN):
            self.engine.cursor_index += 1
        elif key in CONFIRM_KEYS:
            return self.engine.excute_option()


class EquipmentEventHandler(AskUserEventHandler):

    TITLE = "Put Off Equipment"

    def __init__(self, engine):
        super().__init__(engine)

    def on_render(self) -> None:
        super().on_render()

        content = ''
        for i, t in enumerate(self.engine.player.equipment.gears):
            key = t[0]
            val = t[1]
            item_key = chr(ord("a") + i)
            if val is None:
                content += f'({item_key}) {key}: null\n'
            else:
                content += f'({item_key}) {key}: {val.name}\n'
                content += f'        └ {val.attributes}\n'
            render_one_window(self.TITLE, content)

    def on_key_press(self, key, modifiers) -> Optional[Action]:
        player = self.engine.player
        index = key - arcade_key.A

        if 0 <= index <= 26:
            try:
                selected_item = player.equipment.gears[index][1]
            except IndexError:
                self.engine.message_log.add_message(
                    "Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().on_key_press(key, modifiers)

    def on_item_selected(self, gear: Gear) -> Optional[Action]:
        """Called when the user selects a valid item."""
        return actions.PutDownAction(self.engine.player, gear)
