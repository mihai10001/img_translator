from detect_lang import detect_language


def pipeline(string, user_options):
    if user_options.get('detect_lang'):
        lang, prob = detect_language(string)
    if user_options.get('spell_checker'):
        corrected_string = spell_check(string)
