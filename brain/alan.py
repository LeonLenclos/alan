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
import logging
import datetime, time
import wave
import chatterbot
from chatterbot.conversation import Statement
import pygame
import random
import traceback

from logic import MainLogicAdapter
from output import MainOutputAdapter

from test.simple_talk import test

# Init pygame.mixer in order to play wav sounds
pygame.mixer.init()

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
        #log
        self.log('ALAN: initialization', True)
        self.log('time = {}'.format(time.strftime("%d/%m/%Y %H:%M")))

        # load settings
        self.log('SETTINGS:', True)
        self.settings = {}
        if not settings_files: self.load_settings()
        elif type(settings_files) == list:
            for settings_file in settings_files:
                self.load_settings(settings_file)
        elif type(settings_files) == str: self.load_settings(settings_files)
        else : raise('TypeError', 'setting_files must be list or str')



        # Alan vars
        self.age = self.get_age()
        self.lines_of_code = self.get_lines_of_code()
        self.last_results=[]
        self.user_name = None
        self.error_messages = self.settings.get('error_messages', None)


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


    def get_age(self):
        """Return the age of Alan in french"""
        age = ''
        age_time = datetime.datetime.now() - self.birth
        years, months = age_time.days // 365, age_time.days // 30
        if years > 0:
            age += "%s an" % years
            if years > 1: age += "s"
            if months > 0: age += " et"
        if months > 0: age += "%s mois" % months
        return age

    def get_lines_of_code(self):
        """Return the number of lines in the code of Alan"""
        lines_of_code = 0
        for root, dirs, files in os.walk("."):
           for name in files:
              if name.endswith(('.py', '.json', '.rive')):
                  path = '/'.join((root,name))
                  lines_of_code += sum(1 for line in open(path))
        return lines_of_code

    def log(self, message, header=False):
        """
        Print something in the log file.
        """
        with open('log.txt', 'a') as fi:
            if header:
                fi.write('\n' * 2 + '-' * 10)
            fi.write('\n' + message)

    def load_settings(self, settings_file='default', recursion=0):
        """
        Load settings from a file to the settings attribute
        settings_file is a string, the name of the json file without extension
        """
        file_name = "settings/%s.json" % settings_file
        if not os.path.isfile(file_name):
            file_name = "settings/%s/default.json" % settings_file
        self.log('load settings file : {}{}'.format('- '*recursion, file_name))
        with open(file_name, "r") as file:
            # load json
            try:
                file_settings = json.load(file)
            except json.decoder.JSONDecodeError as e:
                raise json.decoder.JSONDecodeError(
                    '{} in {}'.format(e.msg, file_name), e.doc, e.pos)
            # loop keys
            for k in file_settings:
                # if import, do load_settings (recursive)
                if k == 'import':
                    for import_file in file_settings[k]:
                        self.load_settings(import_file, recursion + 1)
                # else, add setting to self.settings
                elif k in self.settings and type(self.settings[k]) == list:
                    self.settings[k] += file_settings[k]
                else:
                    self.settings[k] = file_settings[k]

    def status(self):
        """Return all you need to know about this instance of Alan"""
        return "%s v%s" % (self.name, self.version)

    def get_response(self, input_item, conversation_id=None, listener=None):
        """
        Return the bot's response based on the input.
        :param input_item: An input value.
        :param conversation_id: The id of a conversation.
        :returns: A response to the input.
        :rtype: Statement
        """

        command_regex = r"\*(.+)\*"

        def listen(input_item):
            # Process input if no input item
            if input_item: input = Statement(input)
            else: input = self.input.process_input()

            # Preprocess the input statement
            self.log('PREPROCESS:', True)
            self.log('before = {}'.format(input))
            for pre in self.preprocessors:input = pre(self, input)
            self.log('after  = {}'.format(input))
            return input

        def say(output):
            # clean commands
            text = output.text
            output.text = re.sub(command_regex, "", output.text)

            # Process the response output with the output adapter
            self.output.process_response(output, conversation_id)

            # restore the response text
            output.text = text

        # Get conversation
        if not conversation_id:
            if not self.default_conversation_id:
                self.default_conversation_id = self.storage.create_conversation()
            conversation_id = self.default_conversation_id

        try:
            # Listen
            if listener: listener.send(state='listening')
            input = listen(input_item)

            # Think
            if listener: listener.send(state='thinking')
            output = self.logic.process(input)

            # Speak
            if listener: listener.send(state='speaking')
            say(output)
            if listener: listener.send(state='waiting')

            # Store response
            self.storage.add_to_conversation(conversation_id, input, output)

            # Execute command
            command = re.search(command_regex, output.text)
            if command: self.execute_command(command.group(1))

        except(KeyboardInterrupt, EOFError, SystemExit):
            raise
        except:
            if self.error_messages:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log("ERROR:", True)
                self.log('\n'.join(traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback)))
                say(Statement(random.choice(self.error_messages)))
                self.quit()
            else:
                raise

        return output

    def execute_command(self, command):
        """Execute a special alan's command."""
        self.log('execute command: {}'.format(command))
        if command == 'quit' : self.quit()
        elif command == 'todo' : self.todo()
        elif command == 'info' : self.info()
        elif command == 'rst': self.reset() # reset
        elif command == "music":
            pygame.mixer.Sound("./ressources/musique_generative.wav").play()
        else : raise(KeyError, "The {} command does not exist".format(command))

    def quit(self):
        """Quit Alan."""
        sys.exit()

    def reset(self):
        """Reset Alan."""
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def todo(self):
        """Write 4 last statements in the todo file."""
        count = len(self.last_results) if len(self.last_results) < 6 else 6
        with open("../todo", "a") as f:
            f.write('\n'*3 + '\n'.join([
                ('> ' if i%2 != count%2 else '') +
                self.storage.get_latest_statement(offset=i+2).text
                for i in reversed(range(count))
            ]))

    def info(self):
        """Print informations about last response."""
        infos = "[Pas d'informations disponibles]"
        if len(self.last_results) >= 2:
            infos = ""
            for result in self.last_results[-2]:
                infos += "\n---\n%(logic_identifier)s (%(logic_type)s)\n" % result
                if "text" in result:
                    if result["not_allowed_to_repeat"]:
                        infos += "NOT ALLOWED TO REPEAT"
                    infos += "(%(confidence).2f) '%(text)s'" % result
                else: infos += "NOT PROCESSING"
        print(infos)

    def main_loop(self):
        """Run the main loop"""
        while True:
            try:
                self.get_response(None)
            except(KeyboardInterrupt, EOFError, SystemExit):
                break

def main():
    # Arguments parsing
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', action='store_true', help="Mode Test")
    ap.add_argument('-s', nargs='+', help="Settings file json files without file extension separed with spaces", default=["default"])

    args = ap.parse_args()
    settings_files = args.s

    # Mode verbose


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
