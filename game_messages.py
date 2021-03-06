import libtcodpy as libtcod

import textwrap


class Message:
    """
    Encapsulates a message that is meant to be shown in the MessageLog.
    """
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    """
    Will hold the log of messages from all actions.
    """
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Splits the message if necessary, among multiple lines.
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one.
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color.
            self.messages.append(Message(line, message.color))