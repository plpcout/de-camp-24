FROM python:3.9.1

RUN apt install wget
RUN pip install sqlalchemy pandas psycopg2

WORKDIR /app
COPY hw_ingest_data.py hw_ingest_data.py

ENTRYPOINT [ "python", "hw_ingest_data.py" ]
