from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter
import re

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
        self.speed = kwargs.get("speed", 0.85)
        self.substitutions = kwargs.get("substitutions", {})

    def process_response(self, statement, callback, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        
        pico_statement = statement.text
        pico_statement = self.pico_substitution(pico_statement)
        subprocess.Popen(['sh', 'voice_audio.sh', pico_statement, self.speed])
        callback();
        return statement
    
    
    def pico_substitution(self, pico_statement):
        for original, remplacement in self.substitutions.items():
            pico_statement = re.sub(original, remplacement, pico_statement, flags=re.I)
        return pico_statement
        
    def music(self, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The music.
        """
        subprocess.Popen(['sh', 'music.sh', self.speed])
