from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import re
import utils
import time
import random

class CheckConceptAdapter(AlanLogicAdapter):
    """This adapter check if one of the concepts stored in his database is
    in statement, if it is, he says what he knows about this concept. That is
    he says if the concept is related (or reverse related) to another concept
    and the nature of this relation"""

    def __init__(self, **kwargs):
        """Required kwarg :

        ignore
        A list of strings,
        A list of concepts that are known by alan but that are not
        processed by this adapter (for example if another adapter do it better)

        context_aime
        A list of strings.
        A list of sentences that will give a context to the information gived
        about the concept, when the concept is related to another by the aime relation.
        The context sentences will be formated and may include :
        - A specifier for concept_A founded in statement: `%(A)s`
        - A specifier for concept_B related to concept_A: `%(B)s`
        - A specifier for the relation '%(rel)s'
        e.g.  "Il me semble que %(A)s %(rel)s %(B)s.",

        contexte_est
        A list of strings.
        A list of sentences that will give a context to the information gived
        about the concept, when the concept is related to another by the est relation.
        The context sentences will be formated and may include :
        - A specifier for concept_A founded in statement: `%(A)s`
        - A specifier for concept_B related to concept_A: `%(B)s`
        - A specifier for the relation '%(rel)s'
        e.g.  "Je crois savoir que %(A)s %(rel)s %(B)s.",
        """

        super().__init__(**kwargs)

        # Getting ignore
        try:
            self.ignore = kwargs['ignore']
        except KeyError:
            raise KeyError('ignore  is a required argument')
        if type(self.ignore) != list:
            raise TypeError("ignore must be a list")

        # Getting context_est
        try:
            self.context_est = kwargs['context_est']
        except KeyError:
            raise KeyError('context_est  is a required argument')
        if type(self.context_est) != list:
            raise TypeError("context_est must be a list")

        # Getting context_aime
        try:
            self.context_aime = kwargs['context_aime']
        except KeyError:
            raise KeyError('context_aime  is a required argument')
        if type(self.context_aime) != list:
            raise TypeError("context_aime must be a list")



    def can_process(self, statement):


        # Process only if one of the concepts stored are in the statement
        liste_concept_storage = self.chatbot.storage.list_concept()
        self.liste_concept_statement=[]
        for i in range(0,len(liste_concept_storage)-1):
            if liste_concept_storage[i] in statement.text:
                if not liste_concept_storage[i] in self.ignore:
                    self.liste_concept_statement.append(liste_concept_storage[i])

        if len(self.liste_concept_statement)== 0:
            return False
        else:
            return True
    def process(self, statement):
        concept_A = random.choice(self.liste_concept_statement)
        concept_B = self.chatbot.storage.get_related_concept(concept_A, "est")
        if concept_B :
            relation = "est"
        else:
            concept_B = self.chatbot.storage.get_related_concept(concept_A,
             "est", reverse=True)
            if concept_B :
                x = concept_A
                concept_A = concept_B
                concept_B = x
                relation = "est"
            else:
                concept_B = self.chatbot.storage.get_related_concept(concept_A, "est",negative=True)
                if concept_B :
                    relation = "n'est pas"
                else:
                    concept_B = self.chatbot.storage.get_related_concept(concept_A,
                     "est", reverse=True,negative=True)
                    if concept_B :
                        x = concept_A
                        concept_A = concept_B
                        concept_B = x
                        relation = "n'est pas"




        if concept_B :
            response = random.choice(self.context_est)
        else :
            response = random.choice(self.context_aime)
            concept_B = self.chatbot.storage.get_related_concept(concept_A, "aime")
            if concept_B :
                relation = "aime"
            else:
                concept_B = self.chatbot.storage.get_related_concept(concept_A,
                 "aime", reverse=True)
                if concept_B :
                    x = concept_A
                    concept_A = concept_B
                    concept_B = x
                    relation = "aime"
                else :
                    concept_B = self.chatbot.storage.get_related_concept(concept_A, "aime", negative=True)
                    if concept_B :
                        relation = "n'aime pas"
                    else:
                        concept_B = self.chatbot.storage.get_related_concept(concept_A,
                         "aime", reverse=True, negative=True)
                        if concept_B :
                            x = concept_A
                            concept_A = concept_B
                            concept_B = x
                            relation = "n'aime pas"



        if concept_B:
            response = response % {"A":concept_A, "B":concept_B, "rel":relation }
            response = re.sub("Alan est","je suis",response)
            response = re.sub("Alan n'est","je ne suis",response)
            response = re.sub("Alan aime","j'aime",response)
            response = re.sub("Alan n'aime","je n'aime",response)
            response = re.sub("aime Alan","m'aime",response)
            response = re.sub("aime pas Alan","m'aime pas",response)

        else:
            return None

        statement_out = Statement(utils.sentencize(response))
        statement_out.confidence = self.max_confidence



        return statement_out
