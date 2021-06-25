possible_detection_methods = {
    # 0: Use the Microsoft Computer Vision API
    '0': 'microsoft',
    # 1: Use the Microsoft Computer Vision advanced API
    '1': 'microsoft_advanced',
    # 2: Use the Google Vision API
    '2': 'google',
    # 3: Use the Google Vision advanced API
    '3': 'google_advanced',
    # 4: Use the Abby API
    '4': 'abbyy',
    # 5: Use the Tesseract SDK
    '5': 'tesseract',
}


detection_methods_full_description = {
    '0': {
        'name': 'microsoft',
        'title': 'Microsoft Computer Vision API',
        'description': 'Word based analysis<br> Yields fast results<br>',
        'logo_image': 'ms_logo.png'
    },
    '1': {
        'name': 'microsoft_advanced',
        'title': 'Microsoft Computer Vision API',
        'description': 'Line based analysis<br> Yields accurate results<br> Recognizes diacritics<br> Tipically used on documents<br>',
        'logo_image': 'ms_logo.png'
    },
    '2': {
        'name': 'google',
        'title': 'Google Vision API',
        'description': 'Word based analysis<br> Yields fast results<br>',
        'logo_image': 'google_logo.png'
    },
    '3': {
        'name': 'google_advanced',
        'title': 'Google Vision API',
        'description': 'Line based analysis<br> Yields accurate results<br> Recognizes diacritics<br> Tipically used on documents<br>',
        'logo_image': 'google_logo.png'
    },
    '4': {
        'name': 'abbyy',
        'title': 'Abbyy API',
        'description': 'Text only analysis<br> Text structured nicely<br>',
        'logo_image': 'abbyy_logo.png'
    },
    '5': {
        'name': 'tesseract',
        'title': 'Tesseract SDK',
        'description': 'Text only analysis<br> Yields instant results <br> Runs locally<br>',
        'logo_image': 'tesseract_logo.png'
    },
}