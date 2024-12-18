FROM python:3.11.8-slim

WORKDIR /spark-test

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]