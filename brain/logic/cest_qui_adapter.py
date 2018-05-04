from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import utils
import re
from random import choice
class CestQuiAdapter(AlanLogicAdapter):
    """This adapter answer to questions about who is someone, that is
    questions concerning the 'est' relation like 'Qui est ... '.
    If he don't know the person that is asked for, Alan asks about who is it.
    """

    def __init__(self, **kwargs):
        """Required kwargs :

        questions
        A list of strings.
        The question that must be answered with this adapter.

        relation
        A list of strings.
        The nature of the questions that must be answered with this adapter

        ask
        A list of strings
        The questions used to ask for a relation for an unknown concept.
        Ask will include a specifier for the concept which is asked :
        "Pourrais tu me dire en quelques mots ce qu'est %(concept_A)s."
         """

        super().__init__(**kwargs)
        # Getting questions
        try:
            self.questions = kwargs['questions']
        except KeyError:
            raise KeyError('questions is a required argument')
        if type(self.questions) != list:
            raise TypeError("questions must be a list")

        # Getting relation
        try:
            self.relation = kwargs['relation']
        except KeyError:
            raise KeyError('relation is a required argument')
        if type(self.relation) != str:
            raise TypeError("relation must be a string")
        # Getting ask
        try:
            self.ask = kwargs['ask']
        except KeyError:
            raise KeyError('ask is a required argument')
        if type(self.ask) != list:
            raise TypeError("ask must be a list")
        # Getting know
        try:
            self.know = kwargs['know']
        except KeyError:
            raise KeyError('know is a required argument')
        if type(self.questions) != list:
            raise TypeError("know must be a list")
        # Getting ignore
        try:
            self.ignore = kwargs['ignore']
        except KeyError:
            raise KeyError('ignore')
        if type(self.questions) != list:
            raise TypeError("ignore")


        #in unknow_concept we will store the concept (the person) if is not known
        self.unknow_concept = None

    def process_done(self, is_selected=False):
        if self.unknow_concept and is_selected:
            cestlui = self.chatbot.logic.get_adapter("cestlui")
            cestlui.concept_asked = self.unknow_concept

    def can_process(self, statement):
        # Process only if the latest statement in the conversation
        # contain the relation
        if self.relation in statement.text :
            if len(statement.text.split(" ")) < 8 :
                if "qui" in statement.text :
                    return True
                elif "Qui" in statement.text :
                    return True

        else :
            return False


    def process(self, statement):


        self.unknow_concept = None

        # Concept_A is the string following the last relation occurence
        concept_A=re.split("est ",statement.text)[1]
        # Remove the punctuation from concept_A except apostrophe "'"
        concept_A=utils.remove_punctuation(concept_A, False)

        # Here, we also remove the words "que" and "qui" because of
        #"qui est ce que" or "c'est qui" questions
        concept_A = re.sub("^(qui)","",concept_A)
        concept_A = re.sub("^(que)","",concept_A)
        # Remove starting and ending spaces
        concept_A=concept_A.strip()
        # Get the interrogative part of the question that is before the concept_A
        # if concept_A is empty, set confidence to 0
        if len(concept_A) != 0:
            question = statement.text.split(concept_A)[0]
            # Remove starting and ending spaces
            question = question.strip()
            # Magic substitution to change things like "ton" into "mon"
            concept_A = utils.magic_sub(concept_A)
            # Get the distance between input statement and questions list
            confidence = utils.compare(question,self.questions)
        else:
            confidence=0

        # If concept_A is related by the relation to another concept, put
        # this concept into concept_B
        concept_B = self.chatbot.storage.get_related_concept(concept_A, self.relation)
        if concept_B :

            # Answer the question

            response = choice(self.know)
        else :
            response = choice(self.ignore) + " " + choice(self.ask)
            #If concept_A is not in the database, put it into unknow concept
            self.unknow_concept = concept_A


        response = response % {"A":concept_A, "B":concept_B, "rel":self.relation }
        response = response + "."
        # Verify that concept_A is non-empty and not to big (more than 3 words),
        #  if it is, then set confidence to 0
        if len(concept_A) == 0 or len(concept_A.split(" "))>4:
            confidence=0


        statment_out = Statement(response)
        statment_out.confidence = self.get_confidence(confidence)

        return statment_out
