FROM python:3.8.3-slim-buster
RUN pip install --upgrade pip
WORKDIR /src
COPY ./src /src
COPY requirements.txt /src/requirements.txt
COPY .env /src/.env
RUN pip install -r requirements.txt
CMD ["python", "main.py"]