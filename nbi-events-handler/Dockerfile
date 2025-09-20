FROM python:3.10

RUN apt-get update || true && apt-get clean

RUN apt-get -y install nano
RUN apt-get -y install netbase
RUN apt-get -y install net-tools
RUN apt-get -y install docker.io

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
RUN mkdir -p logs

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["/usr/local/bin/python3.10", "/app/fastapi_runner.py"]