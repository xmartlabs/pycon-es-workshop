FROM python:3.11.1-slim

COPY requirements.txt /src/
WORKDIR /src

RUN python3 -m pip install --upgrade pip setuptools==67.1.0
RUN apt-get update && apt-get install -y netcat
RUN pip install -r requirements.txt

COPY src/ /src

EXPOSE 8080

CMD sh -c "while ! nc -z elasticsearch 9200; do sleep 1; done && python3 main.py"