import random

from nltk.tokenize import sent_tokenize, word_tokenize
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.utils import remove_stopwords

class QuotationIndex():
    """This is a class for an index of quotations
    It is used by the RevelantQuotation logic adapter"""

    def __init__(self, file, context_sentences):
        """A QuotationIndex must be initialized with :
        - A path to the file containing the quotations
        - A list of sentences that will give a context to the quotations

        the file containing the quotations must be plain text,
        quotations are sentences (ends with a ponctuation sign)

        the context sentences will be formated and may include :
            - a specifier for the quotation : `%(quote)s`
            - a specifier for the relevant word : `%(word)s`
        e.g. "Speaking of %(word)s, do you know that Einstein said %(quote)s"
        """

        self.context_sentences = context_sentences

        # the quotes attribute is a list,
        # each ellement of the list is a dict corresponding to a quote
        # the dict has two ellements :
        #   - a "sent" value containing the quote as a string
        #   - a "word" value containing the quote's words as a list of strings
        self.quotes = []

        # create a item for each sentence in the file
        with open(file) as fi:
            # using nltk's sent_tokenize
            sentences = sent_tokenize(fi.read())
            self.quotes = [dict(sent=s, words=[]) for s in sentences]

        # create the words list for each quote
        for q in self.quotes:
            # using nltk's word_tokenize
            words = word_tokenize(q["sent"])
            # removing stopwords with chatterbot's remove_stopwords
            words = remove_stopwords(words,"french")
            # removing short words (2 or 1 character)
            words = [w for w in words if len(w)>2]
            q["words"] = words



    def get(self, sentence):
        """Take a sentence (str) and return a revelant quotation (str)
        """
        # removing stopwords from the sentence
        words = remove_stopwords(word_tokenize(sentence), "french")
        # search for a quote sharing words with the sentence
        for i, quote in enumerate(self.quotes):
            for w in words :
                if w in quote["words"]:
                    # choose randomly a context sentence
                    context = random.choice(self.context_sentences)
                    # add quotations marks to the quotation
                    quotation = '"%s"' % quote["sent"]
                    # delete the quotation to prevent rambling
                    del self.quotes[i]
                    # return the quote in the context
                    return context % {"quote":quotation, "word":w}
        # if nothing is found :
        return "..."

class RelevantQuotation(LogicAdapter):
    """This logic adapter search for good revelant quotations"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.max_confidence = 1
        self.skill_involved = ""

        # a list of QuotationIndex objects
        self.indexes = []

        self.indexes.append(QuotationIndex("./quotes/einstein.txt",[
            "À propos de %(word)s, Einstein a dit un jour : %(quote)s.",
            "Einstein a dis une belle chose à ce sujet : %(quote)s."]))
        self.indexes.append(QuotationIndex("./quotes/proverbs.txt",[
            "%(quote)s Comme on dit !",
            "Ne dis-t-on pas : %(quote)s ?",
            "Comme dit le proverbe : %(quote)s"]))

    def process(self, statement):

        # choose randomly a QuotationIndex
        reply = random.choice(self.indexes).get(statement.text)

        #
        if reply == "...":
            confidence = 0
        else: confidence = 1
        # Randomly select a confidence between 0 and 1

        selected_statement = Statement(reply)
        selected_statement.confidence = confidence

        return selected_statement
