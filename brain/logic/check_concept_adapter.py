from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import re
import utils
import time

class CheckConceptAdapter(AlanLogicAdapter):
    """This adapter check if one of the concepts stored in his database is
    in statement, if it is, he says what he knows about this concept. That is
    he says if the concept is related (or reverse related) to another concept
    and the nature of this relation"""

    def __init__(self, **kwargs):
        """Required kwarg :
        context
        A list of strings.
        A list of sentences that will give a context to the information gived
        about the concept.
        The context sentences will be formated and may include :
        - A specifier for concept_A founded in statement: `%(concept_A)s`
        - A specifier for concept_B related to concept_A: `%(concept_A)s`
        - A specifier for the relation between both of them: `%(concept_A)s`

        e.g.  "Je penses savoir que %(A)s %(rel)s %(B)s.",
        """

        super().__init__(**kwargs)

        # Getting context_sentences
        self.context_sentences = kwargs['context']


    def can_process(self, statement):


        # Process only if the latest statement of Alan came from kesako,and if
        # this is not the first response of Alan and contain the chain ask and
        #   if the response of the human contain the relation
        liste_concept_storage = self.chatbot.storage.list_concept()
        self.liste_concept_statement=[]
        for i in range(0,len(liste_concept_storage)-1):
            if liste_concept_storage[i] in statement.text:
                self.liste_concept_statement.append(liste_concept_storage[i])

        if len(self.liste_concept_statement)== 0:
            return False
        else:
            return True
    def process(self, statement):

        statment_out = Statement(utils.sentencize(self.liste_concept_statement[0]))


        return statment_out
