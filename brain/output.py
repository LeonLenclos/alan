import subprocess
from chatterbot.output import OutputAdapter

class SpeakOutputAdapter(OutputAdapter):
    """This is an output_adapter to give a voice to the chatbot."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.espeak_settings = dict(
            voice="mb-frezf",
            speed=100,
            pitch=50,
        )
        self.voice = "mb-fr1"
        self.speed = 100
        self.pitch = 50

    def espeak(self, text):
        command = ["espeak",
                   "-s{}".format(self.speed),
                   "-p{}".format(self.pitch),
                   "-v{}".format(self.voice),
                   text]
        rep = subprocess.run(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("okidoki")

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        self.espeak(statement.text)
        return statement
