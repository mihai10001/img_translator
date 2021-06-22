import six
from google.cloud.translate_v2.client import Client
from google.oauth2 import service_account

# Path to your Google Translate Account Token
# Make sure not to make public your Token! ( Very important! Don't make it public on GitHub, etc. )
credentials = service_account.Credentials.from_service_account_file(r'.\\env\\GoogleServiceAccountToken.json')


def google_translate(text, to_language):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = Client(credentials=credentials)
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    translated_results = translate_client.translate(text, target_language=to_language, format_='text')
    detected_langs = [result['detectedSourceLanguage'] for result in translated_results]
    most_probable_language = max(set(detected_langs), key=detected_langs.count)
    return [result['translatedText'] for result in translated_results], most_probable_language
