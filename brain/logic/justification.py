from logic import AlanLogicAdapter
from chatterbot.conversation import Statement

class Justification(AlanLogicAdapter):
    """What this LogicAdapter do"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):


        features = self.question_features(statement.text.lower())
        confidence = self.classifier.classify(features)
        response = Statement('Je n\'ai pas à me justifier !')

        response.confidence = confidence
        return response
