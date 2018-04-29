#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is Alan. You can run this module to talk with Alan.

This module describe the Alan class and contain a main function called when the
module is being run
"""

import argparse
import json
import re
import os
import sys
import datetime
import wave
import chatterbot
import pygame

from logic import MainLogicAdapter
from output import MainOutputAdapter

from test.simple_talk import test

class Alan(chatterbot.ChatBot):
    """
    Alan is a chatbot. It inherit the chatterbot ChatBot class.

    Alan is based on chatterbot but a lot of functionalities are overwritten.
    """

    name = "Alan"
    version_infos = ("1", "1", "0")
    version = '.'.join(version_infos)
    birth = datetime.datetime(2018,1,31)
    author = "Fabien Carbo-Gil, Bertrand Lenclos, Léon Lenclos"

    def __init__(self, settings_files):
        """
        Initialisation for Alan.
        You can pass an alternative settings file by the settings_file argument
        """

        # load settings
        self.settings = {}
        for settings_file in settings_files:
            self.load_settings(settings_file)


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
        self.user_name = None

        # init pygame.mixer in order to play wav sounds
        pygame.mixer.init()
        # create sound objects that Alan can play
        self.musique_generative = pygame.mixer.Sound("./ressources/musique_generative.wav")


        # init chatterbot
        super().__init__(self.name, **self.settings)

        # change from MultiLogicAdapter to MainLogicAdapter
        logic_adapters = self.logic.get_adapters()[:-1]
        self.logic = MainLogicAdapter(**self.settings, chatbot=self)
        self.logic.adapters = logic_adapters

        # For having several output adapters
        self.output = MainOutputAdapter(**self.settings, chatbot=self)
        output_adapter = self.settings.get('output_adapter',
                                           'chatterbot.output.OutputAdapter')
        output_adapters = self.settings.get('output_adapters', [output_adapter])
        for adapter in output_adapters:
            self.output.add_adapter(adapter, **self.settings)

    def load_settings(self, settings_file):
        """
        Load settings from a file to the settings attribute
        settings_file is a string, the name of the json file without extension
        """
        with open("settings/%s.json" % settings_file, "r") as file:
            # load json
            file_settings = json.load(file)

            # loop keys
            for k in file_settings:
                # if import, do load_settings (recursive)
                if k == 'import':
                    for import_file in file_settings[k]:
                        self.load_settings(import_file)
                # else, add setting to self.settings
                elif k in self.settings and type(self.settings[k]) == list:
                    self.settings[k] += file_settings[k]
                else:
                    self.settings[k] = file_settings[k]


    def status(self):
        """Return all you need to know about this instance of Alan"""
        return "%s v%s\nBy %s" % (self.name, self.version, self.author)

    def get_response(self, input_item, conversation_id=None, listener=None):
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
        if listener : listener.send(state='listening')
        if input_item:
            input_statement = chatterbot.conversation.Statement(input_item)
        else:
            input_statement = self.input.process_input()

        if listener : listener.send(state='thinking')

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

        if listener : listener.send(state='speaking')
        # Process the response output with the output adapter
        output = self.output.process_response(response, conversation_id)

        if listener : listener.send(state='waiting')

        # execute command
        if command: self.execute_command(command.group(1))

        return output

    def execute_command(self, command):
        """
        Execute a special alan's command.
        """
        self.logger.info('command "{}" passed by Alan'.format(command))
        if command == 'quit': sys.exit()
        if command == 'todo':
            with open("../todo", "a") as f:
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
        if command == "music":
            self.musique_generative.play()

    def learn_response(self, statement, previous_statement):
        """
        Learn that the statement provided is a valid response.
        """
        # TODO: Is this realy useful ??
        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )
            self.logger.info('Adding "{}" as a response to "{}"'.format(
                statement.text,
                previous_statement.text
            ))

    def main_loop(self):
        while True:
            try:
                self.get_response(None)
            except(KeyboardInterrupt, EOFError, SystemExit):
                break

def main():
    # Arguments parsing
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', action='store_true', help="Mode verbose (depreciated)")
    ap.add_argument('-t', action='store_true', help="Mode Test")
    ap.add_argument('-s', nargs='+', help="Settings file json files without file extension separed with spaces", default=["default"])

    args = ap.parse_args()
    settings_files = args.s

    # Mode verbose
    if args.v:
        import logging
        logging.basicConfig(level=logging.INFO)

    # init Alan
    alan = Alan(settings_files=settings_files)

    # Mode test
    if ap.parse_args().t:
        test(alan)
        # locals()[TEST_MODULE].test(alan)
    else :
        # discussion loop
        print('-'*10, alan.status(), '-'*10, sep="\n")
        alan.main_loop()
        print('\n' + '-'*10)

if __name__ == '__main__':
    main()
