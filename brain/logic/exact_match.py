from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from random import randint

class ExactMatch(AlanLogicAdapter):
    """
    This adaper is for saying something to an exact match.
    """

    def __init__(self, **kwargs):
        """Required kwargs :

        match
        A dict : keys are the match, values are list or str of responses.
         """

        super().__init__(**kwargs)

        # Getting catch
        try:
            self.catch = kwargs['catch']
        except KeyError:
            raise KeyError('catch is a required argument')
        if type(self.catch) != dict:
            raise TypeError("catch must be a dict")

        self.index_selected = None
        self.last_statement = None

    def process_done(self, is_selected=False):
        if is_selected:
            if not self.allowed_to_repeat and \
               self.index_selected is not None and \
               type(self.catch[self.last_statement.text]) == list:
                del self.catch[self.last_statement.text][self.index_selected]
        self.index_selected = None

    def can_process(self, statement):
        if statement.text in self.catch:
            return len(self.catch[statement.text]) > 0
        return False

    def process(self, statement):
        self.last_statement = statement
        if type(self.catch[statement.text]) == str:
            response = self.catch[statement.text]
        if type(self.catch[statement.text]) == list:
            self.index_selected = randint(0, len(self.catch[statement.text])-1)
            response = self.catch[statement.text][self.index_selected]
        statement_out = Statement(response)
        statement_out.confidence = self.get_confidence()
        return statement_out
