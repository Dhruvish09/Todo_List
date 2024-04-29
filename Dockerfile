FROM python:3.8-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt
COPY . .
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
