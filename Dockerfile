FROM nikolaik/python-nodejs:python3.7-nodejs14
ADD . /app
WORKDIR /app
RUN apt-get update && apt-get install zip && pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT [ "./start.sh" ]
