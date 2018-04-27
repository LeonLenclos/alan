from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter

class SlowTerminal(OutputAdapter):
    """This is an output_adapter to give a voice to the chatbot."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.delay = kwargs.get("delay", 0.00005)


    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """

        start_time = clock()

        animation = ' .  ', ' .. ', ' ...', ' .. '
        idx = 0
        waiting_time =  len(statement.text) * self.delay
        while clock() - start_time < waiting_time:
            frame = animation[idx % len(animation)]
            print(frame + "\r" * 4, end="")
            idx += 1
            sleep(0.2)
        print(statement.text)
        return statement
