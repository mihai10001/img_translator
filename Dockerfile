FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update -y
RUN apt-get install tesseract-ocr -y

COPY ./app /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]
