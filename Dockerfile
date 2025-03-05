FROM apache/airflow:2.7.3-python3.10

WORKDIR /app

# Copy entire project structure
COPY . .

RUN pip install -e .

RUN chmod +x /app/data/generate_csv.sh
