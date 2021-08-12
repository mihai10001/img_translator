# ImageTranslator

### Specifications  
Web application that detects text from any given image a.k.a OCR (along with bounding boxes) and translates it into the desired language. Then draws the final result on top of the image, so that the translated text matches with the original  
Similar to Google Translate but contains multiple detection, translation and spelling options  


### Implementation  
Web application made with Python, using the Flask framework in order to build the backend and serve static content (HTML pages)  
Uses Google, Microsoft and ABBY APIs in order to detect text online, or has the option to detect text locally using the Tesseract SDK   
Uses Google Translate API for translations   
JQuery to create frontend interactions  
Bootstrap for styling  

### How to run

**Application**
1. cd /app
2. pip3 install -r requirements.txt
3. python3 server.py


**Docker/Docker-compose**
Just build and run the docker image


**Link**
For easier access, follow this link: [Press me](https://ocr-and-translate.herokuapp.com/)  
Link is disabled since using the APIs is costly, money which I can't afford

