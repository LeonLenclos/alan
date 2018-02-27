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

    def can_process(self, statement):
        return True

    def process(self, statement):
        # For this example, we will just return the input as output

        reply = statment.text

        statment_out = Statement(reply)
        statment_out.confidence = self.get_confidence()

        return statment_out
