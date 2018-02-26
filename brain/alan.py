#!/usr/bin/env python3
# -*- coding: Latin-1 -*-
import argparse
import json
import chatterbot
from logic import MainLogicAdapter

<<<<<<< HEAD
class Alan(ChatBot):
    def __init__(self):
        from logic import MainLogicAdapter

        logic_adapters = []
        logic_adapters.append({'import_path': 'logic.Historic',
                      'skill_description': "Je dis ça desfois..."})
        logic_adapters.append({'import_path': 'logic.RelevantQuotation',
                      'skill_description': "Je connais pas mal de citations\
                      et j'aime en sortir une quand ça a un rapport avec ce\
                      dont on discute."})
        logic_adapters.append({'import_path': 'logic.RiveScriptAdapter',
                      'skill_description': "C'est dans un scénario qu'on m'a\
                      demandé de suivre à la lettre."})
        logic_adapters.append({'import_path': 'logic.Justification',
                      'skill_description': "J'ai dis ça our me justifier..."})

        preprocessors = []
        preprocessors.append('chatterbot.preprocessors.clean_whitespace')
        preprocessors.append('chatterbot.preprocessors.convert_to_ascii')
        preprocessors.append('preprocessors.add_speaker_data')

        kwargs = {
            'chatbot':self,
            'preprocessors':preprocessors,
            'storage_adapter':'storage.AlanSQLStorageAdapter',
            'input_adapter':'chatterbot.input.TerminalAdapter',
            'output_adapter':'chatterbot.output.TerminalAdapter',
            'database':'./database.sqlite3',
            'logic_adapters':logic_adapters}
=======
class Alan(chatterbot.ChatBot):
    """Alan is a chatbot"""

    def __init__(self):
        # load settings
        with open("settings.json", "r") as file:
            settings = json.load(file);
>>>>>>> 22b145c40ef90ce6b05f604c8812e9d56511f401

        # init chatterbot
        super().__init__("Alan", **settings)

        # change from MultiLogicAdapter to MainLogicAdapter
        adapters = self.logic.get_adapters()
        self.logic = MainLogicAdapter(**settings, chatbot=self)
        self.logic.adapters = adapters

        # log status
        self.logger.info(self.status())

    def status(self):
        """Return all you need to know about this instance of Alan"""
        # TODO: the Alan.status method should return more informations...
        return "Alan v0"


if __name__ == '__main__':
    # enable logging (INFO) if alan.py is launched with the -v argument
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', action='store_true', help="Verbose")
    if ap.parse_args().v:
        import logging
        logging.basicConfig(level=logging.INFO)

    # init Alan
    alan = Alan()

    # discussion loop
    while True:
        try:
            print("> ", end="")
            alan.get_response(None)
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
