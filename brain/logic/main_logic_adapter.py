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
            # change coefficient of every logic adapters
            adapter.change_coefficient()

            if adapter.can_process(statement):
                # get response
                output = adapter.process(statement)
                # add logic_identifier as extra_data
                output.add_extra_data("logic_identifier", adapter.identifier)
                # store result
                results.append((output.confidence, output, adapter))
                # log
                self.logger.info(
                    '{} = "{}" (confidence : {})'.format(
                        adapter.identifier, output.text, output.confidence
                    )
                )

                # check if it is the best
                if output.confidence > max_confidence:
                    result = output
                    result_adapter = adapter
                    max_confidence = output.confidence

            else:
                # log
                self.logger.info(
                    '{} = Not processing'.format(adapter.identifier)
                )

        result_adapter.change_coefficient(is_selected=True)
        result.add_extra_data("speaker", "alan") # added by leon
        return result
