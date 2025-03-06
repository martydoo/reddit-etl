FROM apache/airflow:2.10.5
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /opt/airflow

USER root
COPY . .
RUN chmod -R 777 .

ENV PYTHONPATH="/opt/airflow/src"

USER airflow
RUN pip install -e .
