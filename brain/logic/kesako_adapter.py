from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import utils
import re
from random import choice
class KesakoAdapter(AlanLogicAdapter):
    """This adapter answer to questions about the nature of concepts, that is
    questions concerning the 'est' relation like 'Qu'est ce que c'est ... '.
    If he don't know the concept that is asked for, Alan asks about this thing is.
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


        self.unknow_concept = None

    def process_done(self, is_selected=False):
        if self.unknow_concept and is_selected:
            esako = self.chatbot.logic.get_adapter("esako")
            esako.concept_asked = self.unknow_concept

    def can_process(self, statement):
        # Process only if the latest statement in the conversation
        # contain the relation
        return (self.relation in statement.text)

    def process(self, statement):


        self.unknow_concept = None

        # Concept_A is the string following the last relation occurence
        # Here, we also remove the words "que" and "qu'"because of "qu'est ce que
        # c'est que ..." questions and remove the string " quoi " if it begin concept_A (because of "C'est
        # quoi..." questions)
        concept_A = re.sub(".*[ ']"+self.relation+" (qu['e] )*(quoi)*","",
                                                            statement.text)
        # Remove the punctuation from concept_A except apostrophe "'"
        concept_A=utils.remove_punctuation(concept_A, False)


        concept_A = re.sub("^(quoi)","",concept_A)
        # Remove starting and ending spaces
        concept_A=concept_A.strip()
        # Get the interrogative part of the question that is before the concept_A
        question = statement.text.split(concept_A)[0]

        # Get the distance between input statement and questions list
        confidence = utils.compare(question, self.questions)
        print(question)



        concept_B = self.chatbot.storage.get_related_concept(concept_A, self.relation)
        concept_C = self.chatbot.storage.get_related_concept(concept_A,
                                                    self.relation, reverse=True)
        # If concept_A is related by the relation to another concept, put
        # this concept into concept_B
        if concept_B :
            # Answer the question
            options = ["%(A)s %(rel)s %(B)s.",
                       "Je penses savoir que %(A)s %(rel)s %(B)s.",
                       "Ça je sais ! %(A)s %(rel)s %(B)s.",
                       "C'%(rel)s %(B)s."]
            response = choice(options)
            if concept_C :
                options = ["D'ailleurs comme %(C)s %(rel)s %(A)s, %(C)s %(rel)s aussi %(B)s.",
                           "%(C)s aussi %(rel)s %(B)s. Puisque %(C)s %(rel)s %(A)s.",
                           "Je sais aussi que %(C)s %(rel)s %(A)s. Et donc %(C)s %(rel)s %(B)s."]
                response += " " +  choice(options)
        # If a concept is related to concept_A by the relation, put
        # this concept into concept_C
        elif  concept_C:
            # Answer and ask
            options = ["%(C)s %(rel)s %(A)s mais je ne sais pas vraiment ce que %(A)s %(rel)s.",
                       "Je sais que %(C)s %(rel)s %(A)s. Mais ça ne veut pas forcement dire que %(A)s %(rel)s %(C)s.",
                       "%(C)s %(rel)s %(A)s. C'est à peu près tout ce que je sais sur %(A)s."]
            response = choice(options) + " " + choice(self.ask)
            self.unknow_concept = concept_A
        # Else ask for a concept related to concept_A
        else:
            # Answer and ask
            options = ["Personne ne m'a jamais appris ce qu'%(rel)s %(A)s.",
                       "Maintenant que tu me pose la question je m'apperçoit que je ne sais pas vraiment ce qu'%(rel)s %(A)s.",
                       "Je ne sais pas ce qu'est %(A)s.",
                       "%(A)s ? Je ne sais pas exactement..."]
            response = choice(options) + " " + choice(self.ask)
            self.unknow_concept = concept_A


        response = response % {"A":concept_A, "B":concept_B, "C":concept_C, "rel":self.relation }
        # Verify that concept_A is non-empty or to big (more than 4 words),
        #  if it is then change confidence to 0
        if len(concept_A) == 0 or len(concept_A.split(" "))>4:
            confidence=0


        statment_out = Statement(utils.sentencize(response))
        statment_out.confidence = self.get_confidence(confidence)

        return statment_out
