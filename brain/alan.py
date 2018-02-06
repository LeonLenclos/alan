#!/usr/bin/env python3
import argparse

from chatterbot import ChatBot

class Alan(ChatBot):
    def __init__(self):

        logic = []

        logic.append({'import_path': 'logic.Historic',
                      'skill_description': "Je dis ça desfois..."})

        logic.append({'import_path': 'logic.RelevantQuotation',
                      'skill_description': "Je connais pas mal de citations\
                      et j'aime en sortir une quand ça a un rapport avec ce\
                      dont on discute."})

        logic.append({'import_path': 'logic.RiveScriptAdapter',
                      'skill_description': "C'est dans un scénario qu'on m'a\
                      demandé de suivre à la lettre."})


        super().__init__("Alan",
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            input_adapter='chatterbot.input.TerminalAdapter',
            output_adapter='chatterbot.output.TerminalAdapter',
            database='./database.sqlite3',
            logic_adapters=logic)


    def status(self):
        return "Alan v0.0.1 version ultra beta"

if __name__ == '__main__':

    # enable logging (INFO) if alan is launched with the -v argument
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', action='store_true', help="Verbose")
    args = ap.parse_args()
    if args.v:
        import logging
        logging.basicConfig(level=logging.INFO)

    # init Alan
    alan = Alan()

    # print Alan's status
    print("---\n%s\n---" % alan.status())

    # discussion loop
    while True:
        try:
            print("> ", end="")
            alan.get_response(None)
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
    print("\n---\n")
