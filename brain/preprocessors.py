from nltk.tokenize import word_tokenize
from string import punctuation
from utils import remove_accents
from utils import french_dict

def save_original_text(chatbot, statement):
    """Put a copy of the statement.text in extra_data['original']"""
    statement.add_extra_data("original", statement.text)
    return statement

def check_spelling(chatbot, statement):
    """Do a word by word spelling correction."""
    if french_dict:
        tokens = word_tokenize(statement.text)
        checked = []
        for token in tokens:
            if token not in punctuation and not french_dict.check(token):
                suggestions = french_dict.suggest(token)
                suggestion = suggestions[0] if suggestions else None
                if suggestion:
                    if remove_accents(token) == remove_accents(suggestion):
                        token = suggestion
            checked.append(token)
        statement.text = ' '.join(checked)
    return statement

def add_speaker_data(chatbot, statement):
    """Add 'human' to extra_data['speaker']"""
    statement.add_extra_data("speaker", "human")
    return statement

def sub_emoticon(chatbot, statement):
    """substitute a smiley by a 'smiley'"""
    emoticons = {'emoticonheart': ('<3',), 'emoticonother': ('O_O', 'o‑o', 'O_o', 'o_O', 'o_o', 'O-O', '>.<', ':-*', ':*', ':×', ':‑O', ':O', ':‑o', ':o', ':-0', '8‑0', '>:O', ':‑/', ':/', ':‑.', '>:\\', '>:/', ':\\', '=/', '=\\', ':L', '=L', ':S', ':‑|', ':| ', ':$', '://)', '://3', ':‑X', ':X', ':‑#', ':#', ':‑&', ':&', 'O:‑)', 'O:)', '0:‑3', '0:3', '0:‑)', '0:)', '0;^)', '>:‑)', '>:)', '}:‑)', '}:)', '3:‑)', '3:)', '>;)', '>:3', '>;3 ', '|;‑)', '|‑O ', ':‑J'), 'emoticonhappy': (':‑)', ':)', ':-]', ':]', ':-3', ':3', ':->', ':>', '8-)', '8)', ':-}', ':}', ':o)', ':c)', ':^)', '=]', '=)', ':‑D', ':D', '8‑D', '8D', 'x‑D', 'xD', 'X‑D', 'XD', '=D', '=3', 'B^D', ":'‑)", ":') ", ';‑)', ';)', '*-)', '*)', ';‑]', ';]', ';^)', ':‑,', ';D', ':^)'), 'emoticonsad': (':‑(', ':(', ':‑c', ':c', ':‑<', ':<', ':‑[', ':[', ':-||', '>:[', ':{', ':@', '>:(', ';(', ":'‑(", ":'( ", ':^(')}
    for emoticon_repr, emoticon_list in emoticons.items():
        for emoticon in emoticon_list:
            statement.text.replace(emoticon, emoticon_repr)
    return statement
