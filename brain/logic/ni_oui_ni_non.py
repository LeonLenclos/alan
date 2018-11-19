from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from utils import compare
from random import choice

BEGIN, PLAYING, END = 1, 2, 3
class NiOuiNiNon(AlanLogicAdapter):
    """For the game 'ni oui ni non' """

    def __init__(self, **kwargs):
        """Required kwarg :

        previous
        A list of strings. the question that must be answered with this adapter.
        """
        super().__init__(**kwargs)

        # Getting previous
        try:
            self.previous = kwargs['previous']
        except KeyError:
            raise KeyError('previous is a required argument')
        if type(self.previous) != list:
            raise TypeError("previous must be a list")

        self.state = BEGIN

    def can_process(self, statement):
        # Process only if there is a latest statement in the conversation
        prev = self.chatbot.storage.get_latest_statement(speaker="alan")
        if not prev:
            return False
        if self.state == BEGIN:
            if prev.text in self.previous:
                self.state = PLAYING
                return False
        return  self.state == PLAYING

    def process(self, statement):
        # # get previous statement's logic_identifier
        conversation = self.chatbot.conversation_id
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
            return None

        return statement_out

    def process_done(self, is_selected):
        if self.state == BEGIN and is_selected:
            self.state = PLAYING
