from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

class EsakoAdapter(AlanLogicAdapter):
    """This adapter is activated only if Kesako just answered before. If Kesako
     don't know a concept related by "est" to the concept for whom he have been
     called, then he ask to the Human what this concept is.
    Esako just store the concept in storage.json the response and thanks the
    human for this information."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        # Process only if the latest statement of Alan contain the chain
        # "Pourrais tu me décrire en quelques mots ce qu'est "
        question_posee = self.chatbot.storage.get_latest_statement(speaker="alan").text
        return ("Pourrais tu me dire en quelques mots ce qu'est "\
                in statement.text)

    def process(self, statement):
        # Get the unknown concept_A
        concept_A = re.sub(".*(qu'est) ","", question_posee)
        # Get the concept B explained by the Human
        concept_B = re.sub(".*([ ']est ) ","", statement.text)
        # Store the new "est" relation into storage.py
        self.chatbot.storage.store_concept_association(concept_A, "est", concept_B)
        reply = "Merci beaucoup, maintenant je comprends mieux ce qu'est "\
        +concept_A+"."

        statment_out = Statement(reply)
        statment_out.confidence = self.get_confidence(1)

        return statment_out
