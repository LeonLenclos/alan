from chatterbot.logic import MultiLogicAdapter
from collections import Counter
from chatterbot.conversation import Statement

class MainLogicAdapter(MultiLogicAdapter):
    """This is the main logic adapter."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # A copy of MultiLogicAdapter's process with two more lines
    def process(self, statement):
        """
        Returns the output of a selection of logic adapters
        for a given input statement.

        :param statement: The input statement to be processed.
        """
        results = []
        result = None
        max_confidence = -1

        for adapter in self.get_adapters():
            if adapter.can_process(statement):

                output = adapter.process(statement)
                output.add_extra_data("logic", type(adapter)) # added by leon
                results.append((output.confidence, output, ))

                self.logger.info(
                    '{} selected "{}" as a response with a confidence of {}'.format(
                        adapter.class_name, output.text, output.confidence
                    )
                )

                if output.confidence > max_confidence:
                    result = output
                    max_confidence = output.confidence
            else:
                self.logger.info(
                    'Not processing the statement using {}'.format(adapter.class_name)
                )

        # If multiple adapters agree on the same statement,
        # then that statement is more likely to be the correct response
        if len(results) >= 3:
            statements = [s[1] for s in results]
            count = Counter(statements)
            most_common = count.most_common()
            if most_common[0][1] > 1:
                result = most_common[0][0]
                max_confidence = self.get_greatest_confidence(result, results)

        result.confidence = max_confidence
        result.add_extra_data("speaker", "alan") # added by leon
        return result
