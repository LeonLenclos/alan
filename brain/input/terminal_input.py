from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement

class TerminalInput(InputAdapter):
    """
    This is an adapter for simple terminal Input.
    """
    def process_input(self, *args, **kwargs):
        return Statement(input())
