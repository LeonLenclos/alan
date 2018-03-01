from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
from utils import compare
import re

class KesakoAdapter(AlanLogicAdapter):
    """This adapter answer to questions about the nature of concepts, that is
    questions concerning the 'est' relation like 'Qu'est ce que c'est ... '.
    If he don't know the concept that is asked for, Alan asks about this thing is.
    """

    def __init__(self, **kwargs):
        """Required kwarg :

        concepts_file
        A string. The path to the file containing the concepts linked with what
        they are.  The file containing the quotations must be an sql database
        with a lot of complicate things into it. Two tables are stored into the
         database :
          _Into the first, concepts are stored along with an index number.

        questions
        A list of strings.
        The question that must be answered with this adapter.

        relation
        A list of strings.
        The nature of the questions that must be answered with this adapter

        ask
        A list of strings
        The question used to ask for a relation for an unknown concept.
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
        if type(self.relation) != str:
            raise TypeError("ask must be a string")




    def can_process(self, statement):
        # Process only if the latest statement in the conversation
        # contain the relation
        return (self.relation in statement.text)

    def process(self, statement):
        relation=self.relation
        # concept_A is the chain following the last relation occurence
        concept_A = re.sub(".*([ ']"+relation+" (que )*)","",statement.text)
        # Remove the chain " quoi " from concept_A (because of "C'est quoi..."
        # questions)
        concept_A = re.sub("^(quoi)","",concept_A)

        # The following block allow the kezako adapter to answer to the "Qu'est
        # ce que..." and "Qu'est ce qu'..." questions.
        # Because this questions can have another meaning if a verb follow the
        # question e.g in "Qu'est ce que tu fais"
        # If you uncomment the block, don't forget to add this two questions to
        # the questions into the settings.json file
        #   #Remove the chain " ce que " from concept_A (because of "Qu'est ce
        #    que..." questions)
        #   concept_A = re.sub("^( ce que )","",concept_A)
        #   #Remove the chain " ce qu' " from concept_A (because of "Qu'est ce
        #    qu'..." qu'est)
        #   concept_A = re.sub("^( ce qu')","",concept_A)

        # Get the interrogative part of the question that is before the concept_A
        question = statement.text.split(concept_A)[0]
        # Remove the punctuation from concept_A except apostrophe "'"
        concept_A = re.sub(r"[.?:,;!]","",concept_A)
        # Remove starting and ending spaces
        concept_A=concept_A.strip()
        # Get the distance between input statement and questions list
        confidence = compare(question, self.questions)
        # Verify that concept_A is non-empty, if it is then change confidence
        # to 0
        if len(concept_A) == 0:
            confidence=0

        # This block is an idea for recognizing if "Qu'est ce que..." questions
        # are followed by a verb, detecting the presence of "tu"

        # If concept_A is related by the relation to another concept, put
        # this concept into concept_B
        if self.chatbot.storage.get_related_concept(concept_A, self.relation):
            concept_B=self.chatbot.storage.get_related_concept(concept_A,
                                                                relation)
            # Turn the first letter of the concept_A chain to a capital
            concept_A = concept_A.lower().capitalize()
            # Answer the question
            response = concept_A+" "+relation+" "+concept_B+"."

        # If a concept is related to concept_A by the relation, put
        # this concept into concept_B
        elif  self.chatbot.storage.get_related_concept(concept_A, relation,
                                                        reverse=True):
            concept_B = self.chatbot.storage.get_related_concept(concept_A,
                                                        relation, reverse=True)
            # Turn the first letter of the concept_B chain to a capital
            concept_B = concept_B.lower().capitalize()
            # Answer and ask
            response = concept_B+" "+relation+" "+concept_A+\
            " mais je ne sais pas vraiment ce qu'est "+concept_A+". "+\
            self.ask % {"concept_A":concept_A}
        # Else aske for a concept related to concept_A
        else:
            # Answer and ask
            response = "Je ne sais pas ce qu'est "+concept_A+". "+\
            self.ask % {"concept_A":concept_A}

        statment_out = Statement(response)
        statment_out.confidence = self.get_confidence(confidence)

        return statment_out
