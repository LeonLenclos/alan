from chatterbot.logic import MultiLogicAdapter
from collections import Counter
from chatterbot.conversation import Statement
import time

class MainLogicAdapter(MultiLogicAdapter):
    """This is the main logic adapter."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def get_adapter(self, identifier):
        """take an identifier and return the corresponding logic adapter"""
        for a in self.get_adapters():
            if a.identifier == identifier:
                return a

    def process(self, statement):
        """
        Returns the output of a selection of logic adapters
        for a given input statement.

        :param statement: The input statement to be processed.
        """
        results = []
        result = None
        max_confidence = -1
        result_adapter = None

        for adapter in self.get_adapters():
            output = None
            result_info = dict(logic_identifier=adapter.identifier,
                               logic_type=type(adapter).__name__)
            start = time.time()

            if adapter.can_process(statement):

                # get response
                output = adapter.process(statement)

                # add logic_identifier as extra_data
                output.add_extra_data("logic_identifier", adapter.identifier)
                # store result
                result_info["confidence"] = output.confidence
                result_info["text"] = output.text
                # check if the sentence have been said
                result_info["not_allowed_to_repeat"] = False
                if not adapter.allowed_to_repeat:
                    conversation_id = self.chatbot.default_conversation_id
                    same_statement = self.chatbot.storage.get_latest_statement(
                                        conversation_id=conversation_id,
                                        text=output.text,
                                        speaker="alan")
                    if same_statement:
                        result_info["not_allowed_to_repeat"] = True

                # check if it is the best
                if (output.confidence > max_confidence
                        and not result_info["not_allowed_to_repeat"]):
                    result = output
                    result_adapter = adapter
                    max_confidence = output.confidence

            results.append(result_info)

            # timer
            end = time.time()

            # log
            if output:
                self.logger.info(
                    '{} = time:{:.6} confidence:{}\ntext:"{}"'.format(
                        adapter.identifier, end-start, output.text, output.confidence
                    )
                )
            else:
                self.logger.info(
                    '{} = time:{:.6} NOT PROCESSING'.format(
                        adapter.identifier, end-start
                    )
                )

        try:
            for adapter in self.get_adapters():
                adapter.process_done(is_selected=adapter is result_adapter)


            # add speaker data
            result.add_extra_data("speaker", "alan")

            # store last results for analysis
            self.chatbot.last_results.append(results)
            return result
        except AttributeError:
            raise Exception("No response found for '%s'" % statement.text)
