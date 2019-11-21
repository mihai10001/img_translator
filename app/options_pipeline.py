from language.language_detector import detect_language
from language.spell_checker import spell_checker
from language.string_ops import clean


def pipeline(string, user_options):
    string = clean(string)

    if user_options.get('detect_lang'):
        lang, prob = detect_language(string)
    if user_options.get('spell_checker'):
        corrected_string = spell_checker(string)
