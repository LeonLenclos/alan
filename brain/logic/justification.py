from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from utils import compare
from random import choice

class Justification(AlanLogicAdapter):
    """What this LogicAdapter do"""

    def __init__(self, **kwargs):
        """Required kwarg :

        questions
        A list of strings. the question that must be answered with this adapter.

        default_response
        A list of strings. possible response when no response has been found.
        """
        super().__init__(**kwargs)

        # Getting questions
        try:
            self.questions = kwargs['questions']
        except KeyError:
            raise KeyError('questions is a required argument')
        if type(self.questions) != list:
            raise TypeError("questions must be a list")

        # Getting default responses
        try:
            self.default_responses = kwargs['default_responses']
        except KeyError:
            raise KeyError('default_responses is a required argument')
        if type(self.questions) != list:
            raise TypeError("default_responses must be a list")

    def can_process(self, statement):
        # Process only if there is a latest statement in the conversation
        return self.chatbot.storage.count()>0

    def process(self, statement):

        # get the distance between input statement and questions list
        confidence = compare(statement.text, self.questions)

        # default response
        response = choice(self.default_responses)

        # get previous statement's logic_identifier
        conversation = self.chatbot.default_conversation_id
        latest = self.chatbot.storage.get_latest_statement(speaker="alan")
        logic_identifier = latest.extra_data["logic_identifier"]

        # search for this logic adapter and get justification
        if logic_identifier:
            for logic in self.chatbot.logic.get_adapters():
                if logic.identifier:
                    if logic.identifier == logic_identifier:
                        response = logic.justification()
                        break

        statement_out = Statement(response)
        statement_out.confidence = self.get_confidence(confidence)
        return statement_out
