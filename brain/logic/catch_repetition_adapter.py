from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

from random import choice
from utils import compare

class CatchRepetitionAdapter(AlanLogicAdapter):
    """This logic adapter react when the user repeat himself"""

    def __init__(self, **kwargs):
        """Required kwarg :

        sentences
        A dict of list of str.
        the three keys you may set are :
        just_said :
        (the sentences to say when the human repeat something he just said)
        said_in_conversation :
        (the sentences to say when the human repeat something he said in the conv)
        said => OBSOLETE !!

        ignore
        a list of sentences to ignore

        speaker
        A string. "alan" or "human"
        the speaker of the statement we're looking for
        default is None (any body)
        """


        super().__init__(**kwargs)

        # Getting sentences
        try:
            self.sentences = kwargs['sentences']
        except KeyError:
            raise KeyError('sentences is a required argument')

        self.speaker = kwargs.get("speaker", None)
        self.ignore = kwargs.get("ignore", [])

    def can_process(self, statement):
        return len(statement.text.split(" ")) > 2 and statement.text not in self.ignore

    def process(self, statement):

        confidence = 0
        response = ''

        conv_element = {'speaker':self.speaker, 'msg':statement.text, 'finished':True}

        filtred_conv = [conv_element for conv_element in self.chatbot.conversation[:-1]
            if self.speaker is None or conv_element['speaker']==self.speaker]

        # this was in the conversation
        if conv_element in filtred_conv:

            # this was the latest
            if filtred_conv[-1] == conv_element :
                response = choice(self.sentences['just_said'])
                confidence = 1

            else:
                response = choice(self.sentences['said_in_conversation'])
                confidence = 0.5


        else :
            return None
        statement_out = Statement(response)
        statement_out.confidence = self.get_confidence(confidence)
        return statement_out
