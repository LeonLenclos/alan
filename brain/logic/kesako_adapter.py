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
        # concept_A is the chain following the last "est" occurence
        concept_A = re.sub(".*([ ']est)","",statement.text)
        # Remove the chain " quoi " from concept_A (because of "C'est quoi..." questions)
        concept_A = re.sub(" quoi ","",concept_A)

        # The following block allow the kezako adapter to answer to the "Qu'est ce que..." and "Qu'est ce qu'..." questions.
        # Because this questions can have another meaning if a verb follow the question e.g in "Qu'est ce que tu fais"
        # If you uncomment the block, don't forget to add this two questions to the questions into the settings.json file
        #   #Remove the chain " ce que " from concept_A (because of "Qu'est ce que..." questions)
        #   concept_A = re.sub("^( ce que )","",concept_A)
        #   #Remove the chain " ce qu' " from concept_A (because of "Qu'est ce qu'..." questions)
        #   concept_A = re.sub("^( ce qu')","",concept_A)

        # Get the interrogative part of the question that is before the concept_A
        question = statement.text.split(concept_A)[0]
        # Remove the chain "?" from concept_A
        concept_A = re.sub(r"\?","",concept_A)

        # Get the distance between input statement and questions list
        confidence = compare(question, self.questions)

        #This block is an idea for recognizing if "Qu'est ce que..." questions are followed by a verb, detecting the presence of "tu"
        #   verbtest = max(compare(question, "Qu'est ce que tu"))
        #   if confidence < verbtest :
        #       confidence=0

        # If concept_A is related by the relation "est" to another concept, put this concept into concept_B
        if self.chatbot.storage.get_related_concept(concept_A, "est") != None:
            concept_B=self.chatbot.storage.get_related_concept(concept_A, "est")
            # Turn the first letter of the concept_A chain to a capital
            concept_A = concept_A.lower().capitalize()
            response = concept_A+" est "+concept_B+"."
        elif  self.chatbot.storage.get_related_concept(concept_A, "est", reverse=true) != None:
            concept_B = self.chatbot.storage.get_related_concept(concept_A, "est", reverse=true)
            # Turn the first letter of the concept_B chain to a capital
            concept_B = concept_B.lower().capitalize()
            response = concept_B+" est "+concept_A+" mais je ne sais pas vraiment ce qu'est"+concept_A+"."
        else:
            response = "Je ne sais pas ce qu'est "+concept_A+"."

        statment_out = Statement(response)
        statment_out.confidence = self.get_confidence(confidence)

        return statment_out
