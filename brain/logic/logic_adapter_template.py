#
# This is a model for Alan's logics adapters
# See :
# http://chatterbot.readthedocs.io/en/stable/logic/create-a-logic-adapter.html
#

from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

class TheLogicAdapterName(AlanLogicAdapter):
    """What this LogicAdapter do"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):
        # For this example, we will just return the input as output

        reply = statement.text

        statment_out = Statement(reply)
        statment_out.confidence = self.get_confidence()

        return statment_out
