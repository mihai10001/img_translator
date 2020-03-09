from googletrans import Translator


def g_translate(string, to_language, from_language=None):
    # Translate the text using googletrans
    # It is a library that implements the Google Translate API
    # Auto generates a 'ticket' in order to make API calls
    translator = Translator()

    # Used togheter with language_detect.py
    # Will use it's own autodetect if from_language is not provided
    if from_language:
        return translator.translate(string, src=from_language, dest=to_language).text
    else:
        return translator.translate(string, dest=to_language).text


def g_bulk_translate(string_list, to_language, from_language=None):
    # Similar to the above, but will bulk translate an array of strings ('texts')
    # Advantage: one bigger API call than a lot of smaller ones
    translator = Translator()

    if from_language:
        translations = translator.translate(string_list, src=from_language, dest=to_language)
    else:
        translations = translator.translate(string_list, dest=to_language)

    return [(result.origin, result.text) for result in translations]
