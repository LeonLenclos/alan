from nltk.tokenize import word_tokenize
import enchant
from string import punctuation

# Init dictionnary for check_spelling
french_dict = enchant.Dict('fr')
dict_extension = ['todo', 'rst', 'quit']
for d in dict_extension : french_dict.add_to_session(d)

def save_original_text(chatbot, statement):
    """Put a copy of the statement.text in extra_data['original']"""
    statement.add_extra_data("original", statement.text)
    return statement

def check_spelling(chatbot, statement):
    """Do a word by word spelling correction."""
    tokens = word_tokenize(statement.text)
    checked = []
    for token in tokens:
        if token not in punctuation:
            if not french_dict.check(token):
                token = french_dict.suggest(token)[0]
        checked.append(token)
    statement.text = ' '.join(checked)
    return statement

def add_speaker_data(chatbot, statement):
    """Add 'human' to extra_data['speaker']"""
    statement.add_extra_data("speaker", "human")
    return statement
