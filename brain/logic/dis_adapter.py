from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from random import randint

class Dis(AlanLogicAdapter):
    """
    This adaper is for tell Alan to say something.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        return statement.text.startswith('dis ')

    def process(self, statement):
        response = statement.text[3:]
        statement_out = Statement(response)
        statement_out.confidence = self.get_confidence()
        return statement_out
