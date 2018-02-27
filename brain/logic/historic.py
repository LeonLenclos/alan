from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

class Historic(AlanLogicAdapter):
    """Ce LogicAdapter retourne une réponse 'Tu viens de me dire...'"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        statment_out = Statement("")
        if statement.text == "Qu'est-ce que je viens de dire":
            statment_out.text = "Tu viens de me dire : \"%s\"" % statement
            statment_out.confidence = self.get_confidence(1)
        elif statement.text == "t'as dit quoi ?":
            conversation = self.chatbot.default_conversation_id
            latest = self.chatbot.storage.get_latest_statement(speaker="alan",
                                                               offset=0)
            if latest:
                statment_out.text = "Je viens de dire : \"%s\"" % latest.text
                statment_out.confidence = self.get_confidence(1)
        else:
            statment_out.confidence = self.get_confidence(0)


        return statment_out
