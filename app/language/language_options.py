from language.language_detect import detect_language
from language.spell_check import spell_check
from language.string_ops import clean
from language.translate import g_bulk_translate


def apply_options(string_list, user_options):
    resulted_string_list = None

    if user_options.get('detect_lang'):
        spell_check_option = user_options.get('spell_check')
        detected_results = [detection_pipeline(string, spell_check_option) for string in string_list]
        resulted_string_list = [el[0] for el in detected_results]
        detected_langs = [el[1] for el in detected_results]
        most_probable_language = max(set(detected_langs), key=detected_langs.count)


    if user_options.get('translate'):
        to_language = user_options.get('translate_to')
        if user_options.get('detect_lang'):
            resulted_string_list = translation_pipeline(resulted_string_list, to_language, most_probable_language)
        else:
            resulted_string_list = translation_pipeline(string_list, to_language)

    return resulted_string_list


def detection_pipeline(string, spell_check_option=None):
    string = clean(string)
    lang, prob = detect_language(string)

    if spell_check_option:
        string = spell_check(string, lang)

    return (string, lang)


def translation_pipeline(string_list, to_lang, from_lang=None):
    if from_lang:
        return g_bulk_translate(string_list, to_lang, from_lang)
    else:
        return g_bulk_translate(string_list, to_lang)