from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException


def detect_language(string):
    # Detect the languages using the detect_langs() method
    # Returns a list containing <class 'langdetect.language.Language'> objects,
    # which are all possible detected languages, including their probabilites
    try:
        langs = detect_langs(string)
    except LangDetectException:
        return 'error', '0'

    # Get the first element, the most probable detected language
    probable_lang = langs[0]
    probable_lang_str = probable_lang.lang
    probable_lang_prb = probable_lang.prob

    # Return its string representation and probability
    return probable_lang_str, probable_lang_prb
