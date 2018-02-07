#!/usr/bin/env python3
import argparse
from chatterbot import ChatBot

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

        super().__init__("Alan", **kwargs)

        adapters = self.logic.get_adapters()
        self.logic = MainLogicAdapter(**kwargs)
        for adapter in adapters:
            self.logic.adapters.append(adapter)
        self.logic.set_chatbot(self)

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
