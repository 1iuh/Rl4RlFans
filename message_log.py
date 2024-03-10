from typing import List, Tuple

import arcade
import color
import constants


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """The full text of this message, including the count if necessary."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    context: arcade.Text

    def __init__(self) -> None:
        self.messages: List[Message] = []
        self.context = arcade.Text(
            "",
            0,
            0,
            arcade.color.WHITE,  # type: ignore
            12,
            multiline=True,
            width=165,
            font_name=constants.font_name
        )

    def clear(self):
        self.messages.clear()

    def add_message(
        self, text: str,
        fg: Tuple[int, int, int] = color.white,
        *,
        stack: bool = True,
    ) -> None:
        """Add a message to this log.
        `text` is the message text, `fg` is the text color.
        If `stack` is True then the message can stack with a previous message
        of the same text.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, x: int, y: int, lines: int, cursor: int = 0) -> None:
        """Render this log over the given area.
        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`.
        """
        if cursor != 0:
            start = max(0, cursor-lines)
            if start == 0:
                end = lines
            else:
                end = cursor
            self.context.text = "\n".join(
                [m.full_text for m in self.messages[start: end]])
        else:
            self.context.text = "\n".join(
                [m.full_text for m in self.messages[-lines:]])
        self.context.x = x
        self.context.y = y
        self.context.draw()
