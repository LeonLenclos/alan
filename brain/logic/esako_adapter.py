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
        # Getting ask
        try:
            self.ask = kwargs['ask']
        except KeyError:
            raise KeyError('ask is a required argument')
        if type(self.relation) != str:
            raise TypeError("ask must be a string")


    def can_process(self, statement):


        # Process only if the latest statement of Alan contain the chain
        # "Pourrais tu me décrire en quelques mots ce qu'est "
        last_response = self.chatbot.storage.get_latest_statement(speaker="alan")
        if last_response:
            if ("Pourrais tu me dire en quelques mots ce qu'est "\
                in last_response.text):
                if "est" in statement.text:
                    return True

        return False


    def process(self, statement):
        # Get what Alan just asked with kesako
        question_posee = self.chatbot.storage.get_latest_statement(speaker="alan")
        question_posee = question_posee.text
        # Get the unknown concept_A
        concept_A = re.sub(r".*(qu'est) ","", question_posee)
        concept_A = utils.remove_punctuation(str.strip(concept_A))

        # Get the concept B explained by the Human
<<<<<<< HEAD
        concept_B = re.sub(".*([ ']est ) ","", statement.text)
        # Store the new "est" relation into storage.py
        self.chatbot.storage.store_concept_association(concept_A, "est", concept_B)
        reply = "Merci beaucoup, maintenant je comprends mieux ce qu'est "\
        +concept_A+"."
=======
        concept_B = re.sub(r".*([ ']+est )","", statement.text)
        concept_B = utils.remove_punctuation(str.strip(concept_B))


        # Store the new "est" relation between concept_B and concept_B
        self.chatbot.storage.store_concept_association(concept_A, "est", concept_B)
        # choose randomly a context sentence
        context = random.choice(self.context_sentences)
        reply = context % {"concept_A":concept_A}
>>>>>>> 4b4f17ffd260a556a494b18d53bc010b2c80e613

        statment_out = Statement(reply)
        statment_out.confidence = self.get_confidence(1)

        return statment_out
