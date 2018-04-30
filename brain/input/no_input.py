from chatterbot.input import InputAdapter

class NoInput(InputAdapter):
    """
    This is an adapter for no input.
    """
    def process_input(self, *args, **kwargs):
        pass
