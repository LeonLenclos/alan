from chatterbot.conversation import Statement
import rivescript

from logic import AlanLogicAdapter
from utils import clean

class RiveScriptAdapter(AlanLogicAdapter):
    """This logic adapter is an interface to RiveScript
    The .rive files should be in the /rive directory"""

    def __init__(self, **kwargs):
        """take one kwarg : rive_files, a list, the paths to the .rive files"""
        super().__init__(**kwargs)

        # getting rive_file
        try:
            rive_files = kwargs['rive_files']
        except KeyError:
            raise KeyError('rive_files is a required argument')

        self.interpreter = rivescript.RiveScript()

        for f in rive_files:
            self.interpreter.load_file(f)

        self.interpreter.sort_replies()

    def get(self, statement):
        """take a statment and ask a reply to the interpreter"""
        user = "localuser"
        text = clean(statement.text)
        reply = self.interpreter.reply(user, text, errors_as_replies=False);
        return Statement(reply)

    def can_process(self, statement):
        """Return False if a NoMatchError is raised"""
        try:
            self.get(statement)
        except rivescript.exceptions.NoMatchError:
            return False

        return True

    def process(self, statement):
        """Return a reply and a constant confidence"""

        statment_out = self.get(statement)
        statment_out.confidence = self.get_confidence()

        return statment_out
