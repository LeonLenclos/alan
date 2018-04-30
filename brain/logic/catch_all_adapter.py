from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from random import randint

class CatchAllAdapter(AlanLogicAdapter):
    """
    This say something when there is nothing to say.
    """

    def __init__(self, **kwargs):
        """Required kwargs :

        sentences
        A list of strings.
        The sentences to say.
         """

        super().__init__(**kwargs)

        # Getting sentences
        try:
            self.sentences = kwargs['sentences']
        except KeyError:
            raise KeyError('sentences is a required argument')
        if type(self.sentences) != list:
            raise TypeError("sentences must be a list")



    def process_done(self, is_selected=False):
        if is_selected and self.index_selected is not None:
            del self.sentences[self.index_selected]
        self.index_selected = None

    def can_process(self, statement):
        return len(self.sentences) > 0
        
    def process(self, statement):
        self.index_selected = randint(0, len(self.sentences)-1)
        statment_out = Statement(self.sentences[self.index_selected])
        statment_out.confidence = self.get_confidence()

        return statment_out
