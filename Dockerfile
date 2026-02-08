FROM python:3.14-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./core .

RUN pip3 install --upgrade pip && pip install -r requirements.txt

CMD ["python", "manage.py" , "runserver", "0.0.0.0:8000"]