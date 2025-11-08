FROM apache/airflow:2.11.0

COPY blueprint/airflow.requirements.txt .

RUN pip install --no-cache-dir -r ./airflow.requirements.txt