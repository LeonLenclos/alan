from chatterbot.conversation import Statement
import rivescript

from logic import AlanLogicAdapter
from utils import remove_punctuation

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

        # setting interpreter
        self.interpreter = rivescript.RiveScript(utf8=True)

        # loading files
        rive_files.extend([
            './rive/array.rive',
            './rive/person.rive'
        ])
        for f in rive_files:
            self.interpreter.load_file(f)

        # do the sort_reply thing
        self.interpreter.sort_replies()

        # give bot var
        self.interpreter.set_variable("age",
                                      self.chatbot.age)
        self.interpreter.set_variable("lines_of_code",
                                      self.chatbot.lines_of_code)
        self.interpreter.set_variable("version",
                                      self.chatbot.version)


        # cf. get methode
        self.reply = None

    def get(self, statement):
        """take a statment and ask a reply to the interpreter"""
        user = "human"
        text = remove_punctuation(statement.text, False)

        # set last reply as the real reply
        history = self.interpreter.get_uservar(user, "__history__")
        if type(history) is dict:
            latest_reply = self.chatbot.storage.get_latest_statement()
            if latest_reply:
                history["reply"][0] = remove_punctuation(latest_reply.text, False)
        self.interpreter.set_uservar(user, "__history__", history)

        # if self.reply is empty, get a reply if not return the last reply
        if not self.reply:
            self.reply = self.interpreter.reply(user, text, errors_as_replies=False);

        # try to get user_name
        user_name = self.interpreter.get_uservar(user, "name")
        if user_name != "undefined":
            self.chatbot.user_name = user_name

        return Statement(self.reply)

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

        # empty the reply attribute to get a new reply next time
        self.reply = None

        return statment_out
