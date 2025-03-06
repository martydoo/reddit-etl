FROM apache/airflow:2.7.3-python3.10

WORKDIR /opt/airflow

# Copy necessary directories
COPY ./dags ./dags
COPY ./src ./src
COPY ./data ./data
COPY setup.py .

RUN pip install -e .

RUN chmod +x /opt/airflow/data/generate_csv.sh

USER airflow
