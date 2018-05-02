from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from random import choice

class CommandsAdapter(AlanLogicAdapter):
    """
    This adaper is for typing specials command to alan.
    """

    def __init__(self, **kwargs):
        """Required kwargs :

        commands
        A dict : keys are the commands, values are dict or str of responses.
         """

        super().__init__(**kwargs)

        # Getting commands
        try:
            self.commands = kwargs['commands']
        except KeyError:
            raise KeyError('commands is a required argument')
        if type(self.commands) != dict:
            raise TypeError("commands must be a dict")

    def can_process(self, statement):
        return statement.text in self.commands

    def process(self, statement):
        if type(self.commands[statement]) == str:
            response = self.commands[statement]
        if type(self.commands[statement]) == list:
            response = choice(self.commands[statement])
        statment_out = Statement('{}*{}*'.format(response, statement))
        statment_out.confidence = self.get_confidence()
        return statment_out
