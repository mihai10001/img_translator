from language.language_detect import detect_language
from language.spell_check import spell_check
from language.string_ops import clean


def pipeline(string, user_options):
    string = clean(string)

    if user_options.get('detect_lang'):
        lang, prob = detect_language(string)

    if user_options.get('spell_checker'):
        if lang:
            corrected_string = spell_check(string)
