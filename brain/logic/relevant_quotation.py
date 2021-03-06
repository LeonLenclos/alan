import random

from nltk.tokenize import sent_tokenize, word_tokenize
from chatterbot.conversation import Statement

from utils import remove_stopwords, remove_punctuation
from logic import AlanLogicAdapter

class RelevantQuotation(AlanLogicAdapter):
    """This logic adapter search for good revelant quotations"""

    def __init__(self, **kwargs):
        """Required kwarg :

        quotation_file
        A string. The path to the file containing the quotations.
        The file containing the quotations must be plain text.
        Quotations are sentences (ends with a punctuation sign)

        Optional kwarg :

        context
        A list of strings. Default is '%(quote)s'
        A list of sentences that will give a context to the quotations.
        The context sentences will be formated and may include :
        - A specifier for the quotation : `%(quote)s`
        - A specifier for the relevant word : `%(word)s`
        e.g. "Speaking of %(word)s, do you know that Einstein said %(quote)s"
        """

        super().__init__(**kwargs)

        # getting context_sentences
        self.context_sentences = kwargs.get('context', '%(quote)s')

        #getting quotation file
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
            words = (q["sent"].replace('\'', ' ')
                              .replace('’',' ')
                              .split(' '))

            # store the words tagged with a '#' and remove the '#'
            words = [remove_punctuation(w) for w in words if '#' in w]
            q["words"] = words
            # remove also '#' to the sentences
            q["sent"] = q['sent'].replace('#', '')
    def can_process(self, statement):
        """Take a sentence and tell if it can find a quotation"""
        return self.get(statement.text, read_only=True) != None

    def get(self, sentence, read_only=False):
        """Take a sentence (str) and return a revelant quotation (str)
        """
        # little cleaning
        sentence = remove_punctuation(sentence)
        words = word_tokenize(sentence)
        # search for a quote sharing words with the sentence
        for i, quote in enumerate(self.quotes):
            for w in words :
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
        return None

    def process(self, statement):

        # choose randomly a QuotationIndex
        reply = self.get(statement.text)
        confidence = self.get_confidence()

        selected_statement = Statement(reply)
        selected_statement.confidence = confidence

        return selected_statement
