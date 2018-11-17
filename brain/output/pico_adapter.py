from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter

class PicoAdapter(OutputAdapter):
    """
    This is an output_adapter to give a voice to the chatbot.
    With the `Pico` text-to-speach software.
    """
    def __init__(self, **kwargs):
        """
        print_response : a boolean. True if we have to print the response
        voice : the voice (see espeak man)
        speed : the speed (see espeak man)
        """
        super().__init__(**kwargs)
        self.pitch = kwargs.get("pitch", -300)
        self.speed = kwargs.get("speed", 0.83)

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        # setsid is for not showing mbrola errors
        # see : https://stackoverflow.com/a/50072485/8752259
        # add it if you want. (  '_>')

        command_tts = [ 'pico2wave',
                   '-l',
                   'fr-FR',
                   '-w',
                   'tmp.wav', statement.text]
        subprocess.run(command_tts)
        subprocess.run(['sh', 'play_audio.sh', self.speed])
        subprocess.run([ 'rm', 'tmp.wav'])


        return statement
