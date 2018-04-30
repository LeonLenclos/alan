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
        self.logger.info('')
        self.logger.info('-'*10)
        self.logger.info('LOGIC: processing all adapters')
        self.logger.info(
            'input = "{}"'.format(statement.text))

        results = []
        result = None
        max_confidence = -1
        result_adapter = None
        processing_all_start = time.time()
        for adapter in self.get_adapters():

            #log
            self.logger.info('')
            self.logger.info(adapter.identifier)

            output = None
            result_info = dict(logic_identifier=adapter.identifier,
                               logic_type=type(adapter).__name__)
            processing_adapter_start = time.time()

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
            processing_time = int((time.time()-processing_adapter_start)*1000)

            # log
            if processing_time > 0:
                self.logger.info(
                    'processing time = {}ms'.format(processing_time))
            if output:
                self.logger.info(
                    'response        = "{}"'.format(output.text))
                self.logger.info(
                    'confidence      = {}'.format(output.confidence))
                if result_info["not_allowed_to_repeat"]:
                    self.logger.info('not allowed to repeat')

            else:
                self.logger.info('not processing')


        # timer
        processing_time = int((time.time()-processing_all_start)*1000)

        # log
        self.logger.info('')
        self.logger.info('-'*10)
        self.logger.info(
            'LOGIC: result'.format(result_adapter.identifier))
        self.logger.info(
            'response              = "{}"'.format(result.text))
        self.logger.info(
            'logic adapter         = "{}"'.format(result_adapter.identifier))
        self.logger.info(
            'confidence            = {}'.format(result.confidence))
        self.logger.info(
            'total processing time = {}ms'.format(processing_time))


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
