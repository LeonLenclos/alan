from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import rivescript

class RiveScriptAdapter(LogicAdapter):
    """This logic adapter is an interface to RiveScript
    The .rive files should be in the /rive directory"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.interpreter = rivescript.RiveScript()
        self.interpreter.load_directory("./rive")
        self.interpreter.sort_replies()

    def get(self, statement):
        """take a statment and ask a reply to the interpreter"""
        user = "localuser"
        text = statement.text
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

        confidence = 0.8

        statment_out = self.get(statement)
        statment_out.confidence = confidence

        return statment_out
