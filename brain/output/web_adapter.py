# DELETE THIS FILE PLEASE

from chatterbot.output import OutputAdapter
import re

from chatterbot.output import OutputAdapter
from chatterbot.conversation import Statement

import nltk



class WebAdapter(OutputAdapter):
    """This is an output_adapter for the web interface."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def process_response(self, statement, callback, session_id=None):
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
        self.update_output(callback)


        return statement

    def get_current_sent(self):
        return self.current_output[self.current_sentence_index]

    def get_current_reply(self):

        return ' '.join(
            [*self.current_output[:self.current_sentence_index],
            self.get_current_sent()[:self.display_count]]
        )

    def update_output(self, callback):
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
        if self.mute or self.display_count > len(self.get_current_sent()):
            if self.mute or self.current_sentence_index >= len(self.current_output)-1:
                self.chatbot.conversation[-1]['finished'] = True
                self.chatbot.conversation[-1]['msg'] = ' '.join(self.current_output)
                self.display_count = 0
                self.timer = None
                callback()
            else:
                self.current_sentence_index += 1
                # wait for the voice to end
                self.current_pico_process.communicate()
                # start new voice
                self.current_pico_process = self.pico(self.get_current_sent())
                # continue reading
                self.display_count = 0
                self.timer = Timer(self.textspeed, self.update_output, [callback])
                self.timer.start()
        # Else recursively call this function
        else:
            self.chatbot.conversation[-1]['msg'] = self.get_current_reply()
            self.timer = Timer(self.textspeed, self.update_output, [callback])
            self.timer.start()

    def pico(self, txt):
        """
        return process
        """
        if self.mute: return subprocess.Popen(['echo']) #hacky

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
        if self.mute: return;

        subprocess.Popen(['sh', 'music.sh', self.voicespeed])
