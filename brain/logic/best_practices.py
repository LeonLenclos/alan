from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from nltk.tokenize import word_tokenize

from utils import compare
from utils import french_dict

class BestPracticesAdapter(AlanLogicAdapter):
    """This logic adapter search for past statments"""

    def __init__(self, **kwargs):
        """Required kwarg :

        sentence
        A string. the sentence that must be said.

        Optionals :

        min_misspelled

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

        self.min_misspelled = kwargs.get('min_misspelled', 3)
        self.min_letters = kwargs.get('min_letters', 20)

    def can_process(self, statement):
        letters = len(statement.text)
        misspelled = 0
        if french_dict :
            misspelled = sum(1 for w in word_tokenize(statement.text)
                             if french_dict.check(w))
        return misspelled > self.min_misspelled or letters > self.min_letters

    def process(self, statement):
        statment_out = Statement(self.sentence)
        statment_out.confidence = self.get_confidence()
        return statment_out
