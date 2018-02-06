from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

class Historic(LogicAdapter):
    """Ce LogicAdapter retourne une réponse 'Tu viens de me dire...'"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        # Randomly select a confidence between 0 and 1
        confidence = 0.1

        # For this example, we will just return the input as output
        statment_out = Statement("Tu viens de me dire : \"%s\"" % statement)
        statment_out.confidence = confidence

        return statment_out
