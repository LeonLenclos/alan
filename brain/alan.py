#!/usr/bin/env python3
# -*- coding: Latin-1 -*-
import argparse
import json
import chatterbot
from logic import MainLogicAdapter

class Alan(chatterbot.ChatBot):
    """Alan is a chatbot"""

    def __init__(self):
        # load settings
        with open("settings.json", "r") as file:
            settings = json.load(file);

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
