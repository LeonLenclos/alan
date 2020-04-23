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
import utils

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
    version_infos = ("1", "5", "2", "dev")
    version = '.'.join(version_infos)
    birth = datetime.datetime(2018,1,31)
    author = "Fabien Carbo-Gil, Bertrand Lenclos, Léon Lenclos"

    def __init__(self, settings):
        """
        Initialisation for Alan.
        You can pass an alternative settings file by the settings_file argument
        """

        # load settings
        self.settings = settings

        # Alan vars
        self.age = self.get_age()
        self.lines_of_code = self.get_lines_of_code()
        self.last_results=[]
        self.user_name = None
        self.error_messages = self.settings.get('error_messages', None)
        self.close = False

        # init chatterbot
        super().__init__(self.name, **self.settings)

        # change from MultiLogicAdapter to MainLogicAdapter and add preconfigured adapters
        logic_adapters = self.logic.get_adapters()[:-1]
        self.logic = MainLogicAdapter(**self.settings, chatbot=self)
        # logic_adapters.extend(preconfigured_logic_adapters)
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
        # init mode impro
        self.setimpro(0)

        #create conversation
        self.conversation_id = self.get_conversation_id()
        # will store all the conversation (used in web interface)
        self.conversation = []

        #log
        self.log('ALAN')
        self.log('TIME : {}'.format(time.strftime("%d/%m/%Y %H:%M")))
        self.log('STATUS : {}'.format(self.status()))
        self.log('CONFIG : {}'.format(settings['config-name']))
        self.log('LOGIC ADAPTERS :')
        for logic_adapter in self.logic.adapters:
            self.log('\t- {} (class={})'.format(
                logic_adapter.identifier, type(logic_adapter).__name__))
        self.log('', True)


    def get_age(self):
        """Return the age of Alan in french"""
        age = ''
        age_time = datetime.datetime.now() - self.birth
        years = age_time.days // 365
        months = (age_time.days-365*years) // 30
        if years > 0:
            age += "%s an" % years
            if years > 1: age += "s"
            if months > 0: age += " et "
        if months > 0: age += "%s mois" % months
        return age

    def get_lines_of_code(self):
        """Return the number of lines in the code of Alan"""
        lines_of_code = 0
        for root, dirs, files in os.walk("."):
           for name in files:
              if name.endswith(('.py', '.json', '.rive', '.sh', '.html')):
                  path = '/'.join((root,name))
                  lines_of_code += sum(1 for line in open(path) if line != '\n')
        return lines_of_code

    def log(self, message, header=False, short=False):
        """
        Print something in the log file.
        header print a line of `-`
        short print in a separed "short file"
        """
        if short:
            with open('log/conv-{:05d}.txt'.format(self.conversation_id), 'a') as fi:
                fi.write('\n' + message)
        else:
            with open('log/log-{:05d}.txt'.format(self.conversation_id), 'a') as fi:
                if header:
                    fi.write('\n' * 2 + '-' * 70)
                fi.write('\n' + message)


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
        
        self.log("INPUT : {}".format(input))
        self.log("{}".format(input), short=True)

        # Preprocess the input statement
        for pre in self.preprocessors:
            input = pre(self, input)
        self.log("PREPROCESSED INPUT : {}".format(input))

        # Get response
        response = self.logic.process(input)
        self.log("OUTPUT : {}".format(response))
        self.log("> {}".format(response), short=True)
        self.log('', True)

        # Store response
        self.storage.add_to_conversation(self.conversation_id, input, response)

        return response

    def update_input(self, msg, finished):
        """ update the last element of conversation from input"""

        conv_element = {'speaker':'human', 'msg':msg, 'finished':finished}

        # if empty conversation, create element
        if not len(self.conversation):
            self.conversation.append(conv_element)

        # if last element is from alan, create element
        elif self.conversation[-1]['speaker'] == 'alan' and self.conversation[-1]['finished']:
            self.conversation.append(conv_element)
        
        # if last element from human, update elemnent
        elif  self.conversation[-1]['speaker'] == 'human':
            self.conversation[-1] = conv_element

        # call the talk method when finished is true
        if finished:
            self.talk(input=msg)

    def talk_alone(self):
        """Use the last alan's reply as an input for next reply"""
        if self.impro:
            # if empty conversation, create element with empty msg
            if not len(self.conversation):
                self.conversation.append({
                    'speaker':'alan',
                    'msg':'',
                    'finished':finished
                })

            if self.conversation[-1]['finished']:
                self.talk(input=self.conversation[-1]['msg'])

    def talk(self, input=None):
        """
        Use input adapters to get an input, get a response and output the
        response with output adapters.
        """
        if self.close :
            raise EndOfConversation()

        command_regex = r"\*(.+)\*"

        try:
            # Listen
            if input is None:
                input = self.input.process_input()

            # Think
            output = self.get_response(input)

            # Speak
            command = re.search(command_regex, output.text)
            if command: output.add_extra_data("command", command.group(1))
            output.text = re.sub(command_regex, "", output.text)
            if command:
                do_command = lambda: self.execute_command(command.group(1))
            else:
                do_command = lambda: None

            self.output.process_response(output, do_command, self.conversation_id)
            



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
                output = Statement(random.choice(self.error_messages))
                output.add_extra_data("command", "quit")
                self.output.process_response(output, self.conversation_id)
                self.quit()
            else:
                raise
        return output

    def execute_command(self, command):
        """Execute a special alan's command."""
        if command == 'quit' : self.quit()
        elif command == 'bug' : raise ArithmeticError()
        elif command == 'todo' : self.todo()
        elif command == 'info' : self.info()
        elif command == 'rst': self.reset() # reset
        elif command == "music":
            self.output.music()
        elif command == "sing":
            subprocess.run(["sh", "sing.sh"])
        elif command == "bip":
            try :
                subprocess.run(["beep"])
            except FileNotFoundError:
                pass
        elif command == "chut": pass
        elif command.startswith("setmaxconf"):
            self.setmaxconf(*command.split(' ')[1:])
        elif command.startswith("setimpro"):
            self.setimpro(*command.split(' ')[1:])
        else : raise KeyError("The {} command does not exist".format(command))

    def finish(self):
        """Do exit job before quitting"""

        # log the all conversation
        self.log("CONVERSATION :")
        count = self.storage.count_conv(self.conversation_id)
        for i in reversed(range(count)):
            self.log("- " + self.storage.get_latest_statement(offset=i, conversation_id=self.conversation_id).text)

    def quit(self):
        """Quit Alan."""
        self.finish()
        self.close = True;

    def reset(self):
        """Reset Alan."""
        return # OBSOLETE
        self.finish()
        python = sys.executable
        os.system('clear')
        os.execl(python, python, * sys.argv)

    def todo(self):
        """Write 4 last statements in the todo file."""
        count = len(self.last_results) if len(self.last_results) < 6 else 6
        with open(os.path.expanduser("~/alantodo.txt"), "a") as f:
            f.write('\n\n{} - ({})\n'.format(datetime.datetime.now().isoformat(), self.conversation_id))
            f.write('\n'.join([
                ('> ' if i%2 != count%2 else '') +
                self.storage.get_latest_statement(offset=i+2, conversation_id=self.conversation_id).text
                for i in reversed(range(count))
            ]))

    def info(self):
        """Print informations about last response."""
        return # OBSOLETE
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
        if logic_adapter:
            logic_adapter.max_confidence = float(value)

    def setimpro(self, value):
        self.impro = int(value)
        mvoadapter = self.logic.get_adapter('mvochatbot')
        if mvoadapter:
            mvoadapter.confidence_coefficient = self.impro

    def main_loop(self):
        """Run the main loop"""
        while True:
            try:
                self.talk()
            except(KeyboardInterrupt, EOFError, SystemExit, EndOfConversation):
                break


class EndOfConversation(Exception):
    pass

def main():
    # Arguments parsing
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', action='store_true', help="Mode Test")
    ap.add_argument('-s', nargs='+', help="Settings file json files without file extension separed with spaces", default=["default"])

    args = ap.parse_args()
    settings = utils.load_settings(args.s)

    # Mode verbose
    subprocess.run('clear')
    print("Démarrage d'Alan. Merci de patienter...")
    # init Alan
    alan = Alan(settings)

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
        status = alan.status()
        print('-'*len(status), status, '-'*len(status), sep="\n")
        alan.main_loop()
        print('\n' + '-'*len(status))

if __name__ == '__main__':
    main()
