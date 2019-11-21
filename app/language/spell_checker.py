import re
from spellchecker import SpellChecker
from string_ops import word_split, word_join

# Languages supported by pyspellchecker by default
# They are based on frequency list dictionaries, you can easily add more
supported_langs = ['en', 'es', 'de', 'fr', 'pt']


def spell_check(string, language, advanced=False):
    # Spell checking implementation based on the pyspellchecker library
    # Doesn't use the unknown() method, better for my approach (graphs)
    if language in supported_langs:
        spell = SpellChecker(language=language)
        words = word_split(string)

        # If advanced, strips the words from pre and post punctuation,
        # before trying to correct the word. Adds them back afterwards
        # This way, misspelled words can be identified correctly
        if advanced:
            words, punctuations = save_puncts(words)
            words = [spell.correction(word) for word in words]
            words = load_puncts(words, punctuations)
        else:
            words = [spell.correction(word) for word in words]

        return word_join(words)


def save_puncts(words):
    punctuations = []
    for word in words:
        pre_punct = re.search('^[.,;!?()]+', word)
        pos_punct = re.search('[.,;!?()]+$', word)
        pre_punct = pre_punct.group() if pre_punct else ''
        pos_punct = pos_punct.group() if pos_punct else ''
        word.replace(pre_punct, '')
        word.replace(pos_punct, '')
        punctuations.append([pre_punct, pos_punct])
    return words, punctuations


def load_puncts(words, punctuations):
    for i, word in enumerate(words):
        word = punctuations[i][0] + word + punctuations[i][1]
    return words
