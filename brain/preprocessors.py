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
