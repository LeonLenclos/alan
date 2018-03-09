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


        relation
        A list of strings.
        The nature of the questions that must be answered with this adapter

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
        if self.relation in statement.text :
            if "je" not in re.split("[Aa]ime",statement.text)[0] :
                if "j'" not in re.split("[Aa]ime",statement.text)[0] :
                    return True
        else :
            return False



    def process(self, statement):
        # Get the relation
        relation=self.relation
        if (re.match("([Aa]ime[s]*-)|([Aa]ime[s]*[- ]tu )|([Aa]ime[s]*[- ]t[- ]il)",
                                                        statement.text)) :
            if re.match("[Aa]ime[s]*[ -]tu ", statement.text) :
                concept_A="tu"
                concept_B=re.sub(".*[Aa]ime[s][- ]tu ","",statement.text)
                concept_B=utils.remove_punctuation(concept_B, False)
            elif re.match("[Aa]ime[s]*[- ]t[- ]il", statement.text) :
                concept_A=re.split("[Aa]ime[s]*[- ]t[- ]il",statement.text)[0]
                concept_B=re.split("[Aa]ime[s]*[- ]t[- ]il",statement.text)[1]
            else :
                statment_out = Statement()
                statment_out.confidence = self.get_confidence(0)
                return statment_out

        else:
            concept_A=re.split(self.relation,statement.text)[0]
            concept_A=utils.remove_punctuation(concept_A, False)
            # Here, we also remove the "est ce que" expression
            concept_A = re.sub("([eE]st[ -]ce[ -]que)","",concept_A)
            concept_B=re.split(self.relation+"[s]*",statement.text)[1]
            concept_B=utils.remove_punctuation(concept_B, False)
        confidence = 1

        # Here we operate a magic substitution in order to change who is talking
        # e.g we change "tu" by "je"
        concept_A = utils.magic_sub(concept_A)
        concept_B = utils.magic_sub(concept_B)
        concept_C = self.chatbot.storage.get_related_concept(concept_B,
                                            self.relation, reverse=True)

        # If concept_A is related by the relation to concept_B
        if (self.chatbot.storage.is_related_concept(concept_A, self.relation,
                                                    concept_B) is not None) :
            concept_A = concept_A.capitalize()
            if self.chatbot.storage.is_related_concept(concept_A, self.relation,concept_B):
                response = "%(A)s %(rel)s %(B)s."
            else:
                response = "%(A)s n'%(rel)s pas %(B)s."
        elif concept_A == "Alan":
            a=random.random()
            if a<0.5:
                self.chatbot.storage.store_concept_association(concept_A,
                                                            "aime", concept_B)
                response="Oh oui j'%(rel)s %(B)s. Et toi?"
            else:
                self.chatbot.storage.store_concept_association(concept_A,
                                    self.relation, concept_B, negative=True)
                response="Pour être franc %(A)s n'%(rel)s pas %(B)s. Et toi?"
        else:
            # If some C is related to B by the relation
            if self.chatbot.storage.get_related_concept(concept_B,
             self.relation, reverse=True) :

                response = " Je sais que %(C)s %(rel)s %(B)s, mais je ne sais\
                 pas si %(A)s (rel)s %(B)s, tu crois que c'est le cas?"
            elif self.chatbot.storage.get_related_concept(concept_B,
             self.relation, reverse=True) is False :
                  response = " Je sais que %(C)s n'%(rel)s pas %(B)s, mais je\
                   ne sais pas si %(A)s (rel)s %(B)s, tu crois que c'est le cas?"
            else:
                response = " Et bien écoute je ne sais\
pas si %(A)s %(rel)s %(B)s, tu crois que c'est le cas?"

        response = response % {"A":concept_A, "B":concept_B, "C":concept_C,
        "rel":self.relation }
        response = re.sub("Alan aime","j'aime",response)
        response = re.sub("Alan n'aime","je n'aime",response)

        # Verify that concept_A is non-empty or to big (more than 4 words),
        #  if it is then change confidence to 0
        if len(concept_A) == 0 or len(concept_A.split(" "))>4:
            confidence=0


        statment_out = Statement(response.capitalize())
        statment_out.confidence = self.get_confidence(confidence)
        return statment_out
