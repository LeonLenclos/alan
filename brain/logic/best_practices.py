from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from nltk.tokenize import word_tokenize

from utils import compare
from utils import french_dict

class BestPracticesAdapter(AlanLogicAdapter):
    """This logic adapter search for past statments
        requieres french dict in utils
    """

    def __init__(self, **kwargs):
        """Required kwarg :

        sentence
        A string. the sentence that must be said.

        Optionals :

        min_misspelled

        max_wellspelled

        min_letters

        """
        super().__init__(**kwargs)

        # Getting sentence
        try:
            self.sentence = kwargs['sentence']
        except KeyError:
            raise KeyError('sentence is a required argument')
        if type(self.sentence) != str:
            raise TypeError("questions must be a sentence")

        self.min_misspelled = kwargs.get('min_misspelled', 0)
        self.min_misspelled = kwargs.get('max_wellspelled', 100)
        self.min_letters = kwargs.get('min_letters', 20)

    def can_process(self, statement):
        if not french_dict :
            return False

        letters = len(statement.text)

        misspelled = sum(1 for w in word_tokenize(statement.text)
                         if not french_dict.check(w))
        wellspelled = len(word_tokenize(statement.text)) - misspelled

        return misspelled >= self.min_misspelled and wellspelled <= self.max_wellspelled and letters >= self.min_letters

    def process(self, statement):
        statement_out = Statement(self.sentence)
        statement_out.confidence = self.get_confidence()
        return statement_out
