from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

from random import choice
from utils import compare

class Historic(AlanLogicAdapter):
    """This logic adapter search for past statments"""

    def __init__(self, **kwargs):
        """Required kwarg :

        questions
        A list of strings. the question that must be answered with this adapter.

        Optional kwarg :

        context
        A list of strings. Default is '%(quote)s'
        A list of sentences that will give a context to the quotations.
        The context sentences will be formated
        It may include a specifier for the quotation : `%(quote)s`

        speaker
        A string. "alan" or "human"
        the speaker of the statement we're looking for
        default is None (any body)

        offset
        A int. 0 is last statement, 1 is the one before and so on
        default is 0
        """
        super().__init__(**kwargs)

        # Getting questions
        try:
            self.questions = kwargs['questions']
        except KeyError:
            raise KeyError('questions is a required argument')
        if type(self.questions) != list:
            raise TypeError("questions must be a list")

        self.get_latest_kargs = {}
        self.get_latest_kargs["speaker"] = kwargs.get("speaker", None)
        self.get_latest_kargs["offset"] = kwargs.get("offset", 0)

        self.context_sentences = kwargs.get('context', '%(quote)s')

    def can_process(self, statement):
        get_latest = self.chatbot.storage.get_latest_statement
        if(get_latest(**self.get_latest_kargs)):
            return True
        return False

    def process(self, statement):

        statment_out = Statement("")
        confidence = compare(statement.text, self.questions)

        get_latest = self.chatbot.storage.get_latest_statement
        latest = get_latest(**self.get_latest_kargs)
        latest = '"%s"' % latest

        print(latest)
        statment_out.text = choice(self.context_sentences) % {"quote":latest}
        statment_out.confidence = self.get_confidence(confidence)
        return statment_out
