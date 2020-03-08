from time import sleep, clock
import subprocess
from chatterbot.output import OutputAdapter
import re

from threading import Timer
from chatterbot.output import OutputAdapter
from chatterbot.conversation import Statement

from random import choice
import nltk



class PicoWebAdapter(OutputAdapter):
    """This is an output_adapter for the web interface."""

    cough_timer = None
    cough_timing = 60*10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_output = None # will be a list of sentence
        self.current_sentence_index = 0 # the index of the list
        self.display_count = 0
        self.timer = None
        self.textspeed = kwargs.get("text-speed", 0.06)
        self.pitch = kwargs.get("pitch", -300)
        self.voicespeed = kwargs.get("voice-speed", 0.85)
        self.substitutions = kwargs.get("substitutions", {})

        self.cough()
        self.pico("Hm")

    def cough(self):

        sounds = ["Hem...", "Hm...", "Hm... Hm...", "Heum...", "Mh..."]
        if PicoWebAdapter.cough_timer is not None:
            PicoWebAdapter.cough_timer.cancel()
        PicoWebAdapter.cough_timer = Timer(
            PicoWebAdapter.cough_timing,
            self.process_response,
            args=[Statement(choice(sounds))])
        PicoWebAdapter.cough_timer.start()

    def process_response(self, statement, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The response statement.
        """
        if self.chatbot.close:
            return;

        self.cough()

        self.current_output = nltk.tokenize.sent_tokenize(statement.text)
        self.current_sentence_index = 0
        self.display_count = 0

        # ignore if the statement is *chut*
        if "command" in statement.extra_data:
            if statement.extra_data["command"] == "chut":
                return statement

        self.current_pico_process = self.pico(self.get_current_sent())
        self.update_output()


        return statement

    def get_current_sent(self):
        return self.current_output[self.current_sentence_index]

    def get_current_reply(self):
        return ' '.join(
            [*self.current_output[:self.current_sentence_index],
            self.get_current_sent()[:self.display_count]]
        )

    def update_output(self):
        """Update little by little the response in chatbot.conversation"""

        # create the conversation element
        conv_el = {'speaker':'alan','msg':'','finished':False}

        # add the element to the conversation
        try:
            if self.chatbot.conversation[-1]['speaker'] == 'human' \
            or self.chatbot.conversation[-1]['finished']:
                self.chatbot.conversation.append(conv_el)
        except IndexError:
            self.chatbot.conversation.append(conv_el)

        # count the letters
        self.display_count += 1
        
        # If the sentence is finished. check for another sentence
        if self.display_count > len(self.get_current_sent()):
            if self.current_sentence_index >= len(self.current_output)-1:
                self.chatbot.conversation[-1]['finished'] = True
                self.chatbot.conversation[-1]['msg'] = self.get_current_reply()
                self.display_count = 0
                self.timer = None
            else:
                self.current_sentence_index += 1
                # wait for the voice to end
                self.current_pico_process.communicate()
                # start new voice
                self.current_pico_process = self.pico(self.get_current_sent())
                # continue reading
                self.display_count = 0
                self.timer = Timer(self.textspeed, self.update_output)
                self.timer.start()
        # Else recursively call this function
        else:
            self.chatbot.conversation[-1]['msg'] = self.get_current_reply()
            self.timer = Timer(self.textspeed, self.update_output)
            self.timer.start()

    def pico(self, txt):
        """
        return process
        """
        txt = self.make_substitution(txt)
        process = subprocess.Popen(['sh', 'voice_audio.sh', txt, str(self.voicespeed)])

        return process
    
    def make_substitution(self, pico_statement):
        for original, remplacement in self.substitutions.items():
            pico_statement = re.sub(original, remplacement, pico_statement, flags=re.I)
        return pico_statement
        
    def music(self, session_id=None):
        """
        :param statement: The statement that the chat bot has produced in response to some input.
        :param session_id: The unique id of the current chat session.
        :returns: The music.
        """
        subprocess.Popen(['sh', 'music.sh', self.voicespeed])
