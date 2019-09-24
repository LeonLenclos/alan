from chatterbot.conversation import Statement
from logic import AlanLogicAdapter
from utils import remove_punctuation

import importlib
from mvochatbot import evaluate
from mvochatbot import main
from mvochatbot import init
from mvochatbot import temp

import nltk


config_file = "./models/config_qa.ini"
mode, USE_CUDA = init.init_config_getSettings(config_file)
input_lang, output_lang, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, USE_QACORPUS, max_length = main.create_model(config_file, USE_CUDA)
MAX_LENGTH_EVAL, temp_module_name, temp_function_name, n_words = init.init_config_eval(config_file)
temperature_module = importlib.import_module(temp_module_name)
temperature_fun = getattr(temperature_module, temp_function_name)

def mvo(input):
    response, confidence = main.alan_answer(input_string, encoder, decoder, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, USE_QACORPUS, n_words)
    return response

class MVOChatbotAdapter(AlanLogicAdapter):
    """This logic adapter is an interface to MVO chatbot
    https://github.com/mvo-projects/chatbot
    """

    def __init__(self, **kwargs):
        """take one kwarg : config file, a path to the .ini file"""
        super().__init__(**kwargs)


    def process(self, statement):
        """Return a reply and a constant confidence"""
        input_string = statement.text
        try:
            response, confidence = mvo(input_string)
        except RuntimeError:
            response, confidence = mvo("c'est la fête")

        statement_out = Statement(response)
        statement_out.confidence = self.get_confidence()


        return statement_out
