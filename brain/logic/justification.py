#
# This is a model for Alan's logics adapters
# See :
# http://chatterbot.readthedocs.io/en/stable/logic/create-a-logic-adapter.html
#

from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

class Justification(LogicAdapter):
    """What this LogicAdapter do"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = kwargs.get('positive', [
            'pourquoi tu dis ca',
            'pourquoi dis tu ca',
            'pourquoi as tu dis ca',
            'ce que tu dis n\'a aucun sens',
            'je ne comprend pas pourquoi tu dis ca',
            'qu\'est ce qui t\'as fait dire ca'
        ])

        self.negative = kwargs.get('negative', [
            'pourquoi tu est un robot',
            'pourquoi aimes-tu les chapeaux',
            'c\'est super ce que tu dis',
            'ca c\'est bien dit',
            'ca depend des fois',
            'ca ne me dit rien'
            'tu crois pas si bien dire'
        ])

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [
            (self.question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def question_features(self, text):
        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.positive + self.negative).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in self.positive + self.negative:
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )

        for word in text.split():
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def can_process(self, statement):
        return True

    def process(self, statement):
        # For this example, we will just return the input as output
        # self.chatbot.storage.get_latest
        features = self.question_features(statement.text.lower())
        confidence = self.classifier.classify(features)
        response = Statement('Je n\'ai pas à me justifier !')

        response.confidence = confidence
        return response
