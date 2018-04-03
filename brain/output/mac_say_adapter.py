from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter

class MacSayAdapter(OutputAdapter):
    """
    This is an output_adapter to give a voice to the chatbot.
    With the `say` command of the mac.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """

        subprocess.run(['say', statement.text])
        print("\n%s\n" % statement.text)
        return statement
