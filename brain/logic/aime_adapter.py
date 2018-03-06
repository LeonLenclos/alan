from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import utils
import re
import random

class AimeAdapter(AlanLogicAdapter):
    """This adapter answer to questions about what someone or something loves,
     that is questions concerning the 'aime' relation like 'Est ce que concept_A
    aime concept_B'.
    If he don't know if he loves the concept that is asked for, Alan choose
    randomly if he loves it or not. If he don't know if concept_A loves
    concept_B he asks for it with aimeask adaptor"""

    def __init__(self, **kwargs):
        """Required kwarg :

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

        # Getting relation
        try:
            self.relation = kwargs['relation']
        except KeyError:
            raise KeyError('relation is a required argument')
        if type(self.relation) != str:
            raise TypeError("relation must be a string")



    def can_process(self, statement):
        # Process only if the latest statement in the conversation
        # contain the relation
        return (self.relation in statement.text)

    def process(self, statement):
        relation=self.relation
        if (("aime[s]*-" or "aime[s]*[- ]tu " or "aime[s]*[- ]t[- ]il") in
                                                            statement.text):
            if "aime[s]*[ -]tu " in statement.text :
                concept_A="tu"
                concept_B=re.sub(".*aime[- ]tu ","",statement.text)
                concept_B=utils.remove_punctuation(concept_B, False)
            elif "aime[s]*[- ]t[- ]il" in statement.context:
                concept_A=statement.text.split("aime[s]*[- ]t[- ]il")[0]
                concept_B=statement.text.split("aime[s]*[- ]t[- ]il")[1]
            else:
                statment_out = Statement()
                statment_out.confidence = self.get_confidence(0)
                return statment_out

        else:
            concept_A=statement.text.split(self.relation)[0]
            concept_A=utils.remove_punctuation(concept_A, False)
            # Here, we also remove the "est ce que" expression
            concept_A = re.sub("([eE]st[ -]ce[ -]que)","",statement.text)
            concept_B=statement.text.split(self.relation)[1]
            concept_B=utils.remove_punctuation(concept_B, False)
        confidence = 1

        # Here we operate a magic substitution in order to change who is talking
        # e.g we change "tu" by "je"
        concept_A = utils.magic_sub(concept_A)
        concept_B = utils.magic_sub(concept_B)

        # If concept_A is related by the relation to concept_B
        if (utils.is_related_concept(concept_A, self.relation,concept_B)
                                                            is not None) :
            concept_A = concept_A.capitalize()
            if utils.is_related_concept(concept_A, self.relation,concept_B):
                response = "%(A)s %(rel)s %(B)s."
            else:
                response = "%(A)s n'%(rel)s pas %(B)s."
        elif concept_A == Alan:
            if random()<0.5:
                self.chatbot.storage.store_concept_association(concept_A,
                                                            "aime", concept_B)
                response="Oh oui j'%(rel)s %(B)s. Et toi?"
            else:
                self.chatbot.storage.store_concept_association(concept_A,
                                    self.relation, concept_B, negative=True)
                response="Pour être franc %(A)s n'%(rel)s pas %(B)s. Et toi?"
        else:
            # If some C is related to B by the relation
            if self.chatbot.storage.get_related_concept(concept_B,self.relation,
                                                                reverse=True) :
                concept_C = self.chatbot.storage.get_related_concept(concept_B,
                                                    self.relation, reverse=True)
                response = " Je sais que %(C)s %(rel)s %(B)s, mais je ne sais\
                 pas si %(A)s (rel)s %(B)s, tu crois que c'est le cas?"
            else:
                response = " Et bien écoute je ne sais\
                 pas si %(A)s (rel)s %(B)s, tu crois que c'est le cas?"

        response = response % {"A":concept_A, "B":concept_B, "C":concept_C,
        "rel":self.relation }
        # Verify that concept_A is non-empty or to big (more than 4 words),
        #  if it is then change confidence to 0
        if len(concept_A) == 0 or len(concept_A.split(" "))>4:
            confidence=0


        statment_out = Statement(response.capitalize())
        statment_out.confidence = self.get_confidence(confidence)
        return statment_out
