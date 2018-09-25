import os
import tarfile
from contextlib import closing
from xml.etree import ElementTree as etree
import gzip
import datetime
import itertools
import unicodedata
import re

class Lang:
    def __init__(self, name):
        self.name = name
        self.trimmed = False
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "PAD", 1: "SOS", 2: "EOS", 3: "UNK"}
        self.n_words = 4 # Count default tokens

    def index_words(self, sentence):
        for word in sentence.split(' '):
            self.index_word(word)

    def index_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1
            
    def get_index_from_word(self, word):
        if word not in self.word2index:
            return 3
        else:
            return self.word2index[word]

    def get_indexes_from_sentences(self, sentence):
        indexes = []
        for word in sentence:
            indexes.append(self.get_index_from_word(word))
        return indexes

    def get_sentence_from_indexes(self, indexes):
        words = []
        for index in indexes:
            words.append(self.index2word[index])
        return words

    # Remove words below a certain count threshold
    def trim(self, min_count):
        if self.trimmed: return
        self.trimmed = True
        
        keep_words = []
        
        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        #('keep_words %s / %s = %.4f' % (
        #    len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        #))

        # Reinitialize dictionaries
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "PAD", 1: "SOS", 2: "EOS", 3: "UNK"}
        self.n_words = 4 # Count default tokens

        for word in keep_words:
            self.index_word(word)

def normalize_string(s):
    s = unicodedata.normalize('NFC', s.lower().strip())
    s = re.sub(r"([,.!?])", r" \1 ", s)
    s = re.sub(r"œ", r"oe", s)
    s = re.sub(r"æ", r"ae", s)
    s = re.sub(r"'", r"' ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def normalize_input(s, lower=False):
    if not(lower):
        s = unicodedata.normalize('NFC', s.strip())
    else:
        s = unicodedata.normalize('NFC', s.lower().strip())
    s = re.sub(r"([,.!?])", r" \1 ", s)
    s = re.sub(r"œ", r"oe", s)
    s = re.sub(r"æ", r"ae", s)
    s = re.sub(r"'", r"' ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def postProcess(s, lower=False):
    s = unicodedata.normalize('NFC', s.strip())
    s = re.sub("<EOS>", " ", s)
    s = re.sub(r"\s([,.])", r"\1", s)
    s = re.sub(r"([!?;:])", r" \1 ", s)
    s = re.sub("' ", "'", s)
    s = re.sub(r"\s+", r" ", s).strip()
    if lower:
        return s.capitalize()
    return s

def filter_pairs(pairs, MIN_LENGTH, MAX_LENGTH):
    filtered_pairs = []
    for pair in pairs:
        if len(pair[0].split()) >= MIN_LENGTH and len(pair[0].split()) <= MAX_LENGTH \
            and len(pair[1].split()) >= MIN_LENGTH and len(pair[1].split()) <= MAX_LENGTH:
                filtered_pairs.append(pair)
    return filtered_pairs

def readXMLfiles(dpath, delay, td=True, create_qacorpus=False):
    moviepairs = []
    for dirpath, dirs, files in os.walk(dpath, topdown=td):
        for filename in files:
            fname = os.path.join(dirpath,filename)
            if fname.endswith('.gz'):
                with gzip.open(fname, 'rt') as file:
                    tree = etree.ElementTree()
                    try:
                        root = tree.parse(file)
                    except:
                        file.close()
                        continue
                    lastSeqTime = 0.0
                    pairs = []
                    currentpair = []
                    timeList = []
                    for seq in tree.iter("s"):
                        phrase = []
                        timeList.clear()
                        for t in seq.iter("time"):
                            timeList.append(t.get("value"))
                        for word in seq.iter("w"):
                            phrase.append(word.text)
                        if len(timeList) > 0:
                            try:
                                dt = datetime.datetime.strptime(timeList[0], "%H:%M:%S,%f")
                                currentSeqTime = dt.hour * 3600 + dt.minute * 60 + dt.second + 0.000001 * dt.microsecond
                                if lastSeqTime > 0.0 and currentSeqTime > (lastSeqTime + delay):
                                    if len(currentpair) > 0:
                                        currentpair.pop(0)
                                dt = datetime.datetime.strptime(timeList[-1], "%H:%M:%S,%f")
                                lastSeqTime = dt.hour * 3600 + dt.minute * 60 + dt.second + 0.000001 * dt.microsecond
                            except ValueError:
                                continue
                        if create_qacorpus:
                            if (len(currentpair) == 0):
                                if '?' not in phrase:
                                    continue
                        if len(phrase) != 0:
                            if phrase[0] == '-':
                                phrase.pop(0)
                            currentpair.append(phrase)
                            if len(currentpair) == 2:
                                context = ' '.join(map(str, currentpair[0]))
                                answer = ' '.join(map(str, currentpair[1]))
                                pairs.append([context, answer])
                                if create_qacorpus and '?' not in phrase:
                                    currentpair.pop(0)
                                currentpair.pop(0)
                    file.close()
                moviepairs.append(pairs)
    return (moviepairs)


def prepare_data(lang1_name, lang2_name, dpath, MIN_LENGTH, MAX_LENGTH, delay, create_qa=False):
    input_lang = Lang(lang1_name)
    output_lang = Lang(lang2_name)
    moviepairs = []
    for path in dpath:
        moviepairs += readXMLfiles(path, delay, create_qacorpus=create_qa)
    i = 0
    for pairs in moviepairs:
        moviepairs[i] = filter_pairs(pairs, MIN_LENGTH, MAX_LENGTH)
        i += 1
    pairs = list(itertools.chain.from_iterable(moviepairs))
        
    #print("Indexing words...")
    for pair in pairs:
        input_lang.index_words(pair[0])
        output_lang.index_words(pair[1])
    
    #print('Indexed %d words in input language, %d words in output' % (input_lang.n_words, output_lang.n_words))
    return input_lang, output_lang, pairs

def read_qapairs(lang1_name, lang2_name, filename):
    pairs = []
    pair = []
    input_lang = Lang(lang1_name)
    output_lang = Lang(lang2_name)
    with open(filename, "r") as file:
        for line in file:
            if len(pair) == 2:
                pairs.append([pair[0], pair[1]])
                pair.clear()
            else:
                pair += [line.rstrip()]
    for pair in pairs:
        input_lang.index_words(pair[0])
        output_lang.index_words(pair[1])

    #print('Indexed %d words in input language, %d words in output' % (input_lang.n_words, output_lang.n_words))
    return input_lang, output_lang, pairs

def trimpairs(input_lang, output_lang, pairs):
    keep_pairs = []
    for pair in pairs:
        input_sentence = pair[0]
        output_sentence = pair[1]
        keep_input = True
        keep_output = True

        for word in input_sentence.split(' '):
            if word not in input_lang.word2index:
                keep_input = False
                break

        for word in output_sentence.split(' '):
            if word not in output_lang.word2index:
                keep_output = False
                break

        # Remove if pair doesn't match input and output conditions
        if keep_input and keep_output:
            keep_pairs.append(pair)
    #print("Trimmed from %d pairs to %d, %.4f of total" % (len(pairs), len(keep_pairs), len(keep_pairs) / len(pairs)))
    return keep_pairs


