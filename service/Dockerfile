FROM python:3.10

RUN apt-get update && apt-get install -y libpq-dev build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD main.py .

ENTRYPOINT ["python3", "main.py"]
