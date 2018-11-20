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

        statement_out = Statement(reply)
        statement_out.confidence = self.get_confidence()

        return statement_out
