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
        said
        (the sentences to say when the human repeat something alan had already listen)

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
        return len(statement.text) > 2 and statement.text not in self.ignore

    def process(self, statement):

        confidence = 0
        response = ''

        get_latest = self.chatbot.storage.get_latest_statement

        latest = get_latest(
            speaker = self.speaker,
            conversation_id=self.chatbot.default_conversation_id)
        latest_same = get_latest(
            speaker=self.speaker,
            text=statement.text)
        latest_same_in_conv = get_latest(
            speaker=self.speaker,
            text=statement.text,
            conversation_id=self.chatbot.default_conversation_id)

        # statement have once been said by speaker
        if latest_same :
            # this was in all time
            response = choice(self.sentences['said'])
            confidence = 0.3

            # this was in the conversation
            if latest_same_in_conv:
                if latest_same.text == latest_same_in_conv.text:
                    response = choice(self.sentences['said_in_conversation'])
                    confidence = 0.5

            # this was the latest
            if latest :
                if latest_same.text == latest.text:
                    response = choice(self.sentences['just_said'])
                    confidence = 1

        statment_out = Statement(response)
        statment_out.confidence = self.get_confidence(confidence)
        return statment_out
