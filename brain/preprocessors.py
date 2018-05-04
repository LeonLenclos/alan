from nltk.tokenize import word_tokenize
from string import punctuation

try :
    import enchant
    # Init dictionnary for check_spelling
    french_dict = enchant.Dict('fr')
    dict_extension = [
        # commands
        'todo', 'rst', 'quit', 'info',
        # other
        'siri', ]
    for d in dict_extension : french_dict.add_to_session(d)
except ImportError: pass

def save_original_text(chatbot, statement):
    """Put a copy of the statement.text in extra_data['original']"""
    statement.add_extra_data("original", statement.text)
    return statement

def check_spelling(chatbot, statement):
    """Do a word by word spelling correction."""
    try: french_dict
    except NameError:
        raise ImportError('you should have pyenchant to use this function')
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
