import subprocess
from chatterbot.output import OutputAdapter

class SpeakOutputAdapter(OutputAdapter):
    """This is an output_adapter to give a voice to the chatbot."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.voice = kwargs.get('voice', 'mb-fr1')
        self.speed = kwargs.get('speed', 100)
        self.pitch = kwargs.get('pitch', 50)

    def espeak(self, text):
        command = ["espeak",
                   "-s{}".format(self.speed),
                   "-p{}".format(self.pitch),
                   "-v{}".format(self.voice),
                   text
                   ]
        subprocess.run(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        self.espeak(statement.text)
        return statement
