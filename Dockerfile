FROM apache/airflow:latest
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy necessary directories
COPY ./dags ./dags
COPY ./src ./src
COPY ./data ./data
COPY setup.py .

USER root
RUN chmod -R 777 .
RUN chmod +x /opt/airflow/data/generate_csv.sh

USER airflow
RUN pip install -e .
