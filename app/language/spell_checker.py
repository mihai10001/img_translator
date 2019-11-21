from spellchecker import SpellChecker
from string_ops import word_split, word_join

# Languages supported by pyspellchecker by default
# Based on frequency list dictionaries, you can easily add more
supported_langs = ['en', 'es', 'de', 'fr', 'pt']


def spell_check(string, language, advanced=False):
    if language in supported_langs:
        spell = SpellChecker(language=language)
        words = word_split(string)

        words = [spell.correction(word) for word in words]
        return word_join(words)


# def advanced_retain(words):

#     for word in words:


# def advanced_
