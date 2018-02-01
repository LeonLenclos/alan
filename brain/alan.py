#!/usr/bin/env python3
from chatterbot import ChatBot

class Alan(ChatBot):
    """docstring for Alan."""
    def __init__(self):
        super().__init__("Alan",
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            input_adapter='chatterbot.input.TerminalAdapter',
            output_adapter='chatterbot.output.TerminalAdapter',
            database='./database.sqlite3')

        pass

    def status(self):
        return "Alan v1.0.0 version ultra beta"

    def talk(self, message):
        if message == quit:
            return "Ciao !\n[quit]"
        else:
            return self.get_response(message)
            # return "Désolé je ne comprends rien à ce que tu me dis..."

if __name__ == '__main__':


    alan = Alan()

    print("■" * 70)
    print(" Alan le robot trop cool ".center(70, "■"))
    print("■" * 70)

    print(alan.status())

    while True:
        try:
            message = alan.get_response(None)

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

    print("■" * 70)
