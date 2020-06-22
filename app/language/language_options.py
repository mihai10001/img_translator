from babel import Locale
from language.language_detect import detect_language
from language.spell_check import spell_check
from language.string_ops import clean
from language.translate import g_bulk_translate


possible_lang_options = {
    # 0: Translate to [*] (Automatic detection)
    '0': {
        'translate': 'true'
    },
    # 1: Detect lang. + Translate to [*]
    '1': {
        'detect_lang': 'true',
        'translate': 'true'
    },
    # 2: Detect lang. + Spell check + Translate to [*]
    '2': {
        'detect_lang': 'true',
        'spell_check': 'true',
        'translate': 'true'
    },
    # 3: Detect lang. + Spell check
    '3': {
        'detect_lang': 'true',
        'spell_check': 'true'
    },
    # 4: Do nothing (just OCR)
    '4': {}
}


def get_country_language(country):
    return Locale.parse('und_' + country).language


def apply_options(string_list, user_options):
    most_probable_language = None
    resulted_string_list = string_list

    if user_options.get('detect_lang'):
        spell_check_option = user_options.get('spell_check')
        detected_results = [lang_detection_pipeline(string, spell_check_option) for string in string_list]
        resulted_string_list = [el[0] for el in detected_results]
        detected_langs = [el[1] for el in detected_results]
        most_probable_language = max(set(detected_langs), key=detected_langs.count)

    if user_options.get('translate'):
        to_language = user_options.get('translate_to')
        if user_options.get('detect_lang'):
            resulted_string_list, _ = bulk_translate_pipeline(resulted_string_list, to_language, most_probable_language)
        else:
            resulted_string_list, most_probable_language = bulk_translate_pipeline(string_list, to_language)

    return resulted_string_list, most_probable_language


def lang_detection_pipeline(string, spell_check_option=None):
    string = clean(string)
    lang, prob = detect_language(string)

    if spell_check_option:
        string = spell_check(string, lang)

    return (string, lang)


def bulk_translate_pipeline(string_list, to_lang, from_lang=None):
    if from_lang:
        return g_bulk_translate(string_list, to_lang, from_lang)
    else:
        return g_bulk_translate(string_list, to_lang)
