from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from utils import compare
from random import choice

BEGIN, PLAYING, END = 1, 2, 3
class NiOuiNiNon(AlanLogicAdapter):
    """For the game 'ni oui ni non' """

    def __init__(self, **kwargs):
        """Required kwarg :

        questions
        A list of strings. the question that must be answered with this adapter.
        """
        super().__init__(**kwargs)

        # Getting questions
        try:
            self.questions = kwargs['questions']
        except KeyError:
            raise KeyError('questions is a required argument')
        if type(self.questions) != list:
            raise TypeError("questions must be a list")


        self.state = BEGIN

    def can_process(self, statement):
        # Process only if there is a latest statement in the conversation
        return 'non' in statement.text.lower() and 'oui' in statement.text.lower()

    def process_begin(self, statement):
        confidence = compare(statement.text, self.questions)
        statement_out = Statement("Allez ! on fait un Ni Oui Ni Non !")
        statement_out.confidence = confidence
        return statement_out


    def process_playing(self, statement):
        # # get previous statement's logic_identifier
        conversation = self.chatbot.default_conversation_id
        alan_latest = self.chatbot.storage.get_latest_statement(speaker="alan").text
        human_latest = statement.text
        if "oui" in alan_latest or "non" in alan_latest:
            word = "oui" if "oui" in alan_latest else "non"
            statement_out = "Mince ! J'ai perdu... j'ai dis \"%s\"..." % word
            statement_out = Statement(statement_out)
            statement_out.confidence = self.get_confidence()
            self.state = END

        elif "oui" in human_latest or "non" in human_latest:
            word = "oui" if "oui" in human_latest else "non"
            statement_out = "Tu as perdu ! Tu as dis \"%s\" !" % word
            statement_out = Statement(statement_out)
            statement_out.confidence = self.get_confidence()
            self.state = END

        else :
            statement_out = Statement("")
            statement_out.confidence = 0

        return statement_out


    def process_end(self, statement):
        statement_out = Statement("")
        statement_out.confidence = 0
        return statement_out


    def process(self, statement):


        if self.state == BEGIN:
            statement_out = self.process_begin(statement)
        elif self.state == PLAYING:
            statement_out = self.process_playing(statement)
        elif self.state == END:
            statement_out = self.process_end(statement)

        return statement_out

    def process_done(self, is_selected):
        if self.state == BEGIN and is_selected:
            self.state = PLAYING
