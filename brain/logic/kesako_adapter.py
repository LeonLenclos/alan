#
# This is a model for Alan's logics adapters
# See :
# http://chatterbot.readthedocs.io/en/stable/logic/create-a-logic-adapter.html
#

from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from utils import compare
import re

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
        # Process only if there is a latest statement in the conversation containing the chain "est"
        return (self.chatbot.storage.count()>0) and ("est" in statement.text)

    def process(self, statement):
        # concept is the chain following the last "est" occurence
        concept_A = re.sub(".*([ ']est)","",statement.text)
        #
        question = statement.text.split(concept_A)
        # remove the chain " quoi " from concept
        concept_A = re.sub(" quoi ","",concept_A)
        # remove the chain "?" from concept
        concept_A = re.sub(r"\?","",concept_A)
        # Turn the first letter of the concept chain to a capital
        concept_A=concept_A.lower().capitalize()
        # get the distance between input statement and questions list
        question = statement.text.split(concept_A)
        confidence = compare(question, self.questions)


        response = concept+" est un machin truc."






        statment_out = Statement(response)
        statment_out.confidence = self.get_confidence(1)

        return statment_out
