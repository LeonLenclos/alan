import random

from nltk.tokenize import sent_tokenize, word_tokenize
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from utils import remove_stopwords

class RelevantQuotation(LogicAdapter):
    """This logic adapter search for good revelant quotations"""

    def __init__(self, **kwargs):
        """A QuotationIndex must be initialized with :
        - A string : path to the file containing the quotations
        - A list of sentences that will give a context to the quotations

        the file containing the quotations must be plain text,
        quotations are sentences (ends with a ponctuation sign)

        the context sentences will be formated and may include :
            - a specifier for the quotation : `%(quote)s`
            - a specifier for the relevant word : `%(word)s`
        e.g. "Speaking of %(word)s, do you know that Einstein said %(quote)s"
        """

        super().__init__(**kwargs)


        self.max_confidence = kwargs.get('max_confidence', 1)
        self.skill_description = kwargs.get('skill_description', None)
        self.context_sentences = kwargs.get('context', '%(quote)s')

        try:
            quotations_file = kwargs['quotations_file']
        except KeyError:
            raise KeyError('file is a required argument')

        # the quotes attribute is a list,
        # each ellement of the list is a dict corresponding to a quote
        # the dict has two ellements :
        #   - a "sent" value containing the quote as a string
        #   - a "word" value containing the quote's words as a list of strings
        self.quotes = []

        # create a item for each sentence in the file
        with open(quotations_file) as fi:
            # using nltk's sent_tokenize
            sentences = sent_tokenize(fi.read())
            self.quotes = [dict(sent=s, words=[]) for s in sentences]

        # create the words list for each quote
        for q in self.quotes:
            # using nltk's word_tokenize
            words = word_tokenize(q["sent"].replace('\'', ' '))
            # removing stopwords with chatterbot's remove_stopwords
            words = remove_stopwords(words)
            # removing short words (2 or 1 character)
            words = [w for w in words if len(w)>2]
            q["words"] = words

    def can_process(self, statement):
        """Take a sentence and tell if it can find a quotation"""
        return self.get(statement.text, read_only=True) != "..."

    def get(self, sentence, read_only=False):
        """Take a sentence (str) and return a revelant quotation (str)
        """
        # removing stopwords from the sentence
        words = remove_stopwords(word_tokenize(sentence.replace('\'', ' ')))
        # search for a quote sharing words with the sentence
        print(sorted(words, key=len, reverse=True))
        for i, quote in enumerate(self.quotes):
            for w in sorted(words, key=len, reverse=True) :
                if w in quote["words"]:
                    # choose randomly a context sentence
                    context = random.choice(self.context_sentences)
                    # add quotations marks to the quotation
                    quotation = '"%s"' % quote["sent"]
                    if not read_only:
                        # delete the quotation to prevent rambling
                        del self.quotes[i]
                    # return the quote in the context
                    return context % {"quote":quotation, "word":w}
        # if nothing is found :
        return "..."

    def process(self, statement):

        # choose randomly a QuotationIndex
        reply = self.get(statement.text)

        #
        if reply == "...":
            confidence = 0
        else: confidence = self.max_confidence
        # Randomly select a confidence between 0 and 1

        selected_statement = Statement(reply)
        selected_statement.confidence = confidence

        return selected_statement
