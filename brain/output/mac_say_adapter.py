from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter

class MacSayAdapter(OutputAdapter):
    """
    This is an output_adapter to give a voice to the chatbot.
    With the `say` command of the mac.
    """
    def __init__(self, **kwargs):
        """
        print_response : a boolean. True if we have to print the response
        """
        super().__init__(**kwargs)
        self.print_response = kwargs.get("print_response", False)

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        subprocess.run(['say', statement.text])
        if self.print_response:
            print("\n%s\n" % statement.text)
        return statement
