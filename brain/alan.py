#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import re
import os
import sys
import datetime

import chatterbot

from logic import MainLogicAdapter
from test.simple_talk import test

class Alan(chatterbot.ChatBot):
    """
    Alan is a chatbot.
    """

    name = "Alan"
    version_infos = (0, 0, 0)
    version = '.'.join(str(version_infos))
    birth = datetime.datetime(2018,1,31)
    author = "Fabien Carbo-Gil, Bertrand Lenclos, Léon Lenclos"

    def __init__(self, settings_file="settings/base.json"):
        """
        Initialisation for Alan.
        You can pass an alternative settings file by the settings_file argument
        """

        # load settings
        with open(settings_file, "r") as file:
            settings = json.load(file);

        # Alan age
        self.age = ""
        age_time = datetime.datetime.now() - self.birth
        years = age_time.days // 365
        months = age_time.days // 30
        if years > 0:
            self.age += "%s an" % years
            if years > 1:
                self.age += "s"
            if months > 0:
                self.age += " et"
        if months > 0:
            self.age += "%s mois" % months

        # Alan lines count
        self.lines_of_code = 0
        for root, dirs, files in os.walk("."):
           for name in files:
              if name.endswith(('.py', '.json', '.rive')):
                  path = '/'.join((root,name))
                  self.lines_of_code += sum(1 for line in open(path))

        # Alan system attributes
        self.last_results=[]

        # init chatterbot
        super().__init__(self.name, **settings)

        # change from MultiLogicAdapter to MainLogicAdapter
        adapters = self.logic.get_adapters()[:-1]
        self.logic = MainLogicAdapter(**settings, chatbot=self)
        self.logic.adapters = adapters


    def status(self):
        """Return all you need to know about this instance of Alan"""
        return "%s v%s\nBy %s" % self.name, self.version, self.author

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
            input_statement = chatterbot.conversation.Statement(input_item)
        else:
            input_statement = self.input.process_input()

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        # get response
        response = self.logic.process(input_statement)

        # search command
        command_regex = r"\*(.+)\*"
        command = re.search(command_regex, response.text)
        response.text = re.sub(command_regex, "", response.text)

        # store response
        if not self.read_only:
            self.storage.add_to_conversation(conversation_id,
                                            input_statement,
                                            response)

        # Process the response output with the output adapter
        output = self.output.process_response(response, conversation_id)

        # execute command
        if command: self.execute_command(command.group(1))

        return output

    def execute_command(self, command):
        self.logger.info('command "{}" passed by Alan'.format(command))
        if command == 'quit': sys.exit()
        if command == 'todo':
            with open("../todo.md", "a") as f:
                f.write("\n\n```\n> %s\n%s\n> %s\n%s\n```\n"
                    % tuple([self.storage.get_latest_statement(offset=i+2)
                    for i in reversed(range(4))]))
        if command == 'info':
            infos = "\nANALYSIS"
            infos += "\n--------\n"
            user_input = self.storage.get_latest_statement(speaker="human",
                                                           offset=1)
            infos += "\nInput : '%s'\n" % user_input
            for result in self.last_results[-2]:
                infos += "\n---\n"
                infos += "%(logic_identifier)s (%(logic_type)s)\n" % result
                if "text" in result:
                    if result["not_allowed_to_repeat"]:
                        infos += "NOT ALLOWED TO REPEAT "
                    infos += "(%(confidence).2f) '%(text)s'" % result
                else:
                    infos += "NOT PROCESSING"
            infos += "\n---\n"
            print(infos)


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
        test(alan)
        # locals()[TEST_MODULE].test(alan)
    else :
        # discussion loop
        while True:
            try:
                print("> ", end="")
                alan.get_response(None)

            except(KeyboardInterrupt, EOFError, SystemExit):
                break
