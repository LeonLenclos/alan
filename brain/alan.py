#!/usr/bin/env python3
# -*- coding: Latin-1 -*-
import argparse
import json
import chatterbot
from logic import MainLogicAdapter
from chatterbot.conversation import Statement

class Alan(chatterbot.ChatBot):
    """Alan is a chatbot"""

    def __init__(self):
        # load settings
        with open("settings.json", "r") as file:
            settings = json.load(file);

        # init chatterbot
        super().__init__("Alan", **settings)

        # change from MultiLogicAdapter to MainLogicAdapter
        adapters = self.logic.get_adapters()[:-1]
        self.logic = MainLogicAdapter(**settings, chatbot=self)
        self.logic.adapters = adapters

        # log status
        self.logger.info(self.status())

    def status(self):
        """Return all you need to know about this instance of Alan"""
        # TODO: the Alan.status method should return more informations...
        return "Alan v0"

    def get_response(self, input_item, conversation_id=None):
        """
        Return the bot's response based on the input.
        :param input_item: An input value.
        :param conversation_id: The id of a conversation.
        :returns: A response to the input.
        :rtype: Statement
        """

        # Get conversation
        if not conversation_id:
            if not self.default_conversation_id:
                self.default_conversation_id = self.storage.create_conversation()
            conversation_id = self.default_conversation_id

        # Get input
        if input_item:
            input_statement = Statement(input_item)
        else:
            input_statement = self.input.process_input()

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        # get response
        response = self.logic.process(input_statement)

        # store response
        if not self.read_only:
            self.storage.add_to_conversation(conversation_id,
                                            input_statement,
                                            response)

        # Process the response output with the output adapter
        return self.output.process_response(response, conversation_id)

    def learn_response(self, statement, previous_statement):
        """
        Learn that the statement provided is a valid response.
        """

        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )
            self.logger.info('Adding "{}" as a response to "{}"'.format(
                statement.text,
                previous_statement.text
            ))

        # Save the statement after selecting a response

if __name__ == '__main__':
    # enable logging (INFO) if alan.py is launched with the -v argument
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', action='store_true', help="Verbose")
    ap.add_argument('-t', action='store_true', help="Test")

    # Mode verbose
    if ap.parse_args().v:
        import logging
        logging.basicConfig(level=logging.INFO)

    # init Alan
    alan = Alan()

    # Mode test
    if ap.parse_args().t:
        from test import test
        test(alan)
    else :
        # discussion loop
        while True:
            try:
                print("> ", end="")
                alan.get_response(None)
            except(KeyboardInterrupt, EOFError, SystemExit):
                break
