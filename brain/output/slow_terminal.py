from time import sleep, clock
from random import random
import subprocess
from chatterbot.output import OutputAdapter

class SlowTerminal(OutputAdapter):
    """This is an output_adapter to give a voice to the chatbot."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.delay = kwargs.get("delay", 0.002)


    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """


        animation = ' .  ', ' .. ', ' ...', ' .. '
        idx = 0
        waiting_time = self.delay * random()
        start_time = clock()
        while clock() - start_time < waiting_time:
            frame = animation[idx % len(animation)]
            print(frame + "\r" * 4, end="")
            idx += 1
            sleep(0.15)

        print("> {}".format(statement.text))
        return statement
