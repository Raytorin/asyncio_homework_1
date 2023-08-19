FROM python:3.11

WORKDIR /main_app

COPY ./swapi_app .

EXPOSE 5000

CMD pip install -r requirements.txt && \
    python work_db.py && \
    python main.py