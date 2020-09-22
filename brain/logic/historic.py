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
        default is None (anybody)

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

        self.conv_element = {}
        self.speaker = kwargs.get("speaker", None)
        self.offset = kwargs.get("offset", 0)

        self.context_sentences = kwargs.get('context', '%(quote)s')

    def can_process(self, statement):
        conv = [conv_element for conv_element in self.chatbot.conversation
            if self.speaker is None 
            or conv_element['speaker'] == self.speaker]
        if len(conv)>self.offset and compare(statement.text, self.questions) > 0.2:
            return True
        return False

    def process(self, statement):

        statement_out = Statement("")
        confidence = compare(statement.text, self.questions)**2

        conv = [conv_element for conv_element in self.chatbot.conversation
            if self.speaker is None 
            or conv_element['speaker'] == self.speaker]

        latest = conv[-1-self.offset]['msg']

        latest = '"%s"' % latest

        statement_out.text = choice(self.context_sentences) % {"quote":latest}
        statement_out.confidence = self.get_confidence(confidence)
        return statement_out
