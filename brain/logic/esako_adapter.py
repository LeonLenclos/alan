from logic import AlanLogicAdapter
from chatterbot.conversation import Statement
import re
import utils
import random

class EsakoAdapter(AlanLogicAdapter):
    """This adapter is activated only if Kesako just answered before. If Kesako
     don't know a concept related by the relation to the concept for whom he have been
     called, then he ask to the Human what this concept is.
    Esako just store the concept associated with the response given and thanks the
    human for this information."""

    def __init__(self, **kwargs):
        """Required kwarg :

        relation
        A list of strings.
        The nature of the questions that must be answered with this adapter

        ask
        A list of strings
        the question used to ask for a relation for an unknown concept

        context
        A list of strings.
        A list of sentences that will give a context to thanks the Human for
        giving informations.
        The context sentences will be formated and may include :
        - A specifier for concept_A learned : `%(concept_A)s`
        e.g. "Aaaaaaah, c'est donc ça %(concept_A)s."
        """

        super().__init__(**kwargs)

        # Getting context_sentences
        self.context_sentences = kwargs['context']

        # Getting relation
        try:
            self.relation = kwargs['relation']
        except KeyError:
            raise KeyError('relation is a required argument')
        if type(self.relation) != str:
            raise TypeError("relation must be a string")
        
        self.concept_asked = None

    def can_process(self, statement):


        # Process only if the latest statement of Alan came from kesako,and if
        # this is not the first response of Alan and contain the chain ask and
        #   if the response of the human contain the relation


        last_logic=self.chatbot.storage.get_latest_response_extra_data(
                                                extra_data="logic_identifier")
        if self.concept_asked:
            if last_logic == "kesako":
                if self.relation in statement.text:
                    return True
            else :
                self.concept_asked = None
                return False
        else :
            return False

    def process(self, statement):

        # Get the unknown concept_A
        concept_A = self.concept_asked
        self.concept_asked = None

        # Get the concept B explained by the Human
        concept_B = re.sub(r".*([ ']+est )","", statement.text)
        concept_B = utils.remove_punctuation(str.strip(concept_B))
        concept_B = utils.magic_sub(concept_B)


        # Store the new "est" relation between concept_A and concept_B
        self.chatbot.storage.store_concept_association(concept_A, self.relation, concept_B)
        # choose randomly a context sentence
        context = random.choice(self.context_sentences)
        reply = context % {"concept_A":concept_A}
        statement_out = Statement(utils.sentencize(reply))
        statement_out.confidence = self.get_confidence()

        return statement_out
