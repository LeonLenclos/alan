from chatterbot.conversation import Statement
from logic import AlanLogicAdapter
from utils import remove_punctuation

import importlib
from mvochatbot import evaluate
from mvochatbot import main
from mvochatbot import init
from mvochatbot import temp

import nltk




class MVOChatbotAdapter(AlanLogicAdapter):
    """This logic adapter is an interface to MVO chatbot
    https://github.com/mvo-projects/chatbot
    """

    def __init__(self, **kwargs):
        """take one kwarg : config file, a path to the .ini file"""
        super().__init__(**kwargs)

        # getting config_file
        try:
            config_file = kwargs['config_file']
        except KeyError:
            raise KeyError('config_file is a required argument')

        # Get Settings | Parameters 
        mode, self.USE_CUDA = init.init_config_getSettings(config_file)
        self.input_lang, self.output_lang, pairs, self.encoder, self.decoder, encoder_optimizer, decoder_optimizer, criterion, self.USE_QACORPUS, self.max_length = main.create_model(config_file, self.USE_CUDA)
        self.MAX_LENGTH_EVAL, temp_module_name, temp_function_name, self.n_words = init.init_config_eval(config_file)
        temperature_module = importlib.import_module(temp_module_name)
        self.temperature_fun = getattr(temperature_module, temp_function_name)

    def can_process(self, statement):
        """Return False if there is to much word"""
        return len(nltk.tokenize.word_tokenize(statement.text)) <= self.MAX_LENGTH_EVAL 

    def process(self, statement):
        """Return a reply and a constant confidence"""
        input_string = statement.text
        response, confidence = main.alan_answer(input_string, self.encoder, self.decoder, self.input_lang, self.output_lang, self.USE_CUDA, self.max_length, self.temperature_fun, self.USE_QACORPUS, self.n_words)

        #print("mvo confidence : {}".format(confidence))
        statement_out = Statement(response)
        statement_out.confidence = self.get_confidence()


        return statement_out
