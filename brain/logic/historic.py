from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

class Historic(AlanLogicAdapter):
    """Ce LogicAdapter retourne une réponse 'Tu viens de me dire...'"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        # For this example, we will just return the input as output
        statment_out = Statement("Tu viens de me dire : \"%s\"" % statement)
        statment_out.confidence = self.get_confidence()

        return statment_out
