#
# This is a model for Alan's logics adapters
# See :
# http://chatterbot.readthedocs.io/en/stable/logic/create-a-logic-adapter.html
#

from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

class KesakoAdapter(AlanLogicAdapter):
    """This adapator answer to questions about the nature of things, that's questions beginning by 'Qu'est ce que c'est ... '.
    If he don't know the thing that is asked for, Alan asks about this thing and remember the answer """

    def __init__(self, **kwargs):
        """Required kwarg :

        concepts_file
        A string. The path to the file containing the concepts linked with what they are.
        The file containing the quotations must be an sql database with a lot of complicate things into it.
        Two tables are stored into the database :
        _Into the first, concepts are stored along with an index number.

        Optional kwarg :

        questions
        A list of strings. the question that must be answered with this adapter."""

        super().__init__(**kwargs)
        # Getting questions
        try:
            self.questions = kwargs['questions']
        except KeyError:
            raise KeyError('questions is a required argument')
        if type(self.questions) != list:
            raise TypeError("questions must be a list")


    def can_process(self, statement):
        # Process only if there is a latest statement in the conversation
        return {self.chatbot.storage.count()>0} and {"est" in statement}

    def process(self, statement):
        # get the distance between input statement and questions list
        confidence = compare(statement.text, self.questions)

        response = statement.text






        statment_out = Statement(response)
        statment_out.confidence = self.get_confidence(confidence)

        return statment_out
