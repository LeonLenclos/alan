#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is Alan. You can run this module to talk with Alan.

This module describe the Alan class and contain a main function called when the
module is being run
"""

import subprocess
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
import nltk
import random
import traceback

from logic import MainLogicAdapter
from output import MainOutputAdapter

import init_relation

from test.simple_talk import test



# Download needed nltk ressources
try : nltk.data.find('tokenizers/punkt')
except LookupError:
    print('Resource punkt not found (NLTK). So I download it...')
    nltk.download('punkt')

class Alan(chatterbot.ChatBot):
    """
    Alan is a chatbot. It inherit the chatterbot ChatBot class.

    Alan is based on chatterbot but a lot of functionalities are overwritten.
    """

    name = "Alan"
    version_infos = ("1", "2", "2")
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

        # init relations
        init_relation.store_all(self)

        #create conversation
        self.conversation_id = self.get_conversation_id()

        #log
        self.log('ALAN')
        self.log('TIME : {}'.format(time.strftime("%d/%m/%Y %H:%M")))
        self.log('STATUS : {}'.format(self.status()))
        self.log('SETTINGS : {}'.format(settings_files))
        self.log('LOGIC ADAPTERS :')
        for logic_adapter in self.logic.adapters:
            self.log('\t- {} (class={})'.format(
                logic_adapter.identifier, type(logic_adapter).__name__))
        self.log('', True)


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
                  lines_of_code += sum(1 for line in open(path) if line != '\n')
        return lines_of_code

    def log(self, message, header=False):
        """
        Print something in the log file.
        """
        with open('log/conv-{}.txt'.format(self.conversation_id), 'a') as fi:
            if header:
                fi.write('\n' * 2 + '-' * 70)
            fi.write('\n' + message)

    def load_settings(self, settings_file='default', recursion=0):
        """
        Load settings from a file to the settings attribute
        settings_file is a string, the name of the json file without extension
        """
        file_name = "settings/%s.json" % settings_file
        if not os.path.isfile(file_name):
            file_name = "settings/%s/default.json" % settings_file
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
        return "{} v{} ({})".format(self.name, self.version, self.conversation_id)
    
    def get_conversation_id(self):
        """Return a new conversation id"""
        conversation_id = self.storage.create_conversation()
        return conversation_id

    def get_response(self, input):
        """return a response to the input_item"""

        if type(input) != Statement:
            input = Statement(input)

        # Preprocess the input statement
        for pre in self.preprocessors:
            input = pre(self, input)
        self.log("PREPROCESSED INPUT : {}".format(input))

        # Get response
        response = self.logic.process(input)

        # Store response
        self.storage.add_to_conversation(self.conversation_id, input, response)

        return response

    def talk(self, listener=None):
        """
        Use input adapters to get an input, get a response and output the
        response with output adapters.
        """
        command_regex = r"\*(.+)\*"

        try:

            # Listen
            if listener: listener.send(state='listening')
            input = self.input.process_input()
            self.log("INPUT : {}".format(input))

            # Think
            if listener: listener.send(state='thinking')
            output = self.get_response(input)
            self.log("OUTPUT : {}".format(output))
            self.log('', True)

            # Speak
            if listener: listener.send(state='speaking')
            command = re.search(command_regex, output.text)
            output.text = re.sub(command_regex, "", output.text)
            self.output.process_response(output, self.conversation_id)

            # Execute command
            if command:
                self.execute_command(command.group(1))

            # Waiting
            if listener: listener.send(state='waiting')


        # Catch errors and say something funny
        except(KeyboardInterrupt, EOFError, SystemExit): raise
        except:
            if self.error_messages:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log("ERROR :")
                self.log('\n'.join(traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback)))
                self.output.process_response(Statement(random.choice(self.error_messages)), self.conversation_id)
                self.quit()
            else:
                raise

    def execute_command(self, command):
        """Execute a special alan's command."""
        if command == 'quit' : self.quit()
        elif command == 'todo' : self.todo()
        elif command == 'info' : self.info()
        elif command == 'rst': self.reset() # reset
        elif command == "music":
            if self.output.music:
                self.output.music()
        elif command == "bip":
            try :
                subprocess.run(["beep"])
            except FileNotFoundError:
                pass
        elif command.startswith("setmaxconf"):
            self.setmaxconf(*command.split(' ')[1:])
        else : raise(KeyError, "The {} command does not exist".format(command))

    def finish(self):
        """Do exit job before quitting"""

        # log the all conversation
        self.log("CONVERSATION :")
        count = self.storage.count_conv(self.conversation_id)
        for i in reversed(range(count)):
            self.log("- " + self.storage.get_latest_statement(offset=i).text)

    def quit(self):
        """Quit Alan."""
        self.finish()
        sys.exit()

    def reset(self):
        """Reset Alan."""
        self.finish()
        python = sys.executable
        os.system('clear')
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
                if "text" in result:
                    infos += "\n---\n%(logic_identifier)s (%(logic_type)s)\n" % result
                    if result["not_allowed_to_repeat"]:
                        infos += "NOT ALLOWED TO REPEAT"
                    infos += "(%(confidence).2f) '%(text)s'" % result
        print(infos)

    def setmaxconf(self, identifier, value):
        """Set the max confidence of the adapter with the given identifier
        to the given value"""
        logic_adapter = self.logic.get_adapter(identifier)
        logic_adapter.max_confidence = float(value)

    def main_loop(self):
        """Run the main loop"""
        while True:
            try:
                self.talk()
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
    subprocess.run('clear')
    print("Démarrage d'Alan. Merci de patienter...")
    # init Alan
    alan = Alan(settings_files=settings_files)

    # Mode test
    if ap.parse_args().t:
        test(alan)
        # locals()[TEST_MODULE].test(alan)
    else :
        # discussion loop
        subprocess.run('clear')
        try :
            subprocess.run(["beep"])
        except FileNotFoundError:
            pass
        print('-'*10, alan.status(), '-'*10, sep="\n")
        alan.main_loop()
        print('\n' + '-'*10)

if __name__ == '__main__':
    main()
