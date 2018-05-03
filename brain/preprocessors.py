from nltk.tokenize import word_tokenize
import enchant
from string import punctuation
french_dict = enchant.Dict('fr')

def save_original_text(chatbot, statement):
    statement.add_extra_data("original", statement.text)
    return statement

def check_spelling(chatbot, statement):
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
    statement.add_extra_data("speaker", "human")
    return statement
