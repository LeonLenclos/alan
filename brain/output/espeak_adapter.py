from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter

class EspeakAdapter(OutputAdapter):
    """
    This is an output_adapter to give a voice to the chatbot.
    With the `espeak` command of linux.
    """
    def __init__(self, **kwargs):
        """
        print_response : a boolean. True if we have to print the response
        voice : the voice (see espeak man)
        speed : the speed (see espeak man)
        """
        super().__init__(**kwargs)
        self.voice = kwargs.get("voice", 'fr')
        self.speed = kwargs.get("speed", 175)

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        # setsid is for not showing mbrola errors
        # see : https://stackoverflow.com/a/50072485/8752259
        # add it if you want. (  '_>')
        
        command = [ 'espeak',
                   '-v', self.voice,
                   '-s', str(self.speed),
                   statement.text]
        subprocess.run(command)
        return statement
