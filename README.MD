mkdir -p airflow_data/config airflow_data/logs airflow_data/plugins;
psql -h postgres -p 5432 -U airflow -d airflow -W ${POSTGRES_PASSWORD} -c "CREATE DATABASE ${LAKEHOUSE_DB};"
psql -h postgres -p 5432 -U airflow -d airflow -W ${POSTGRES_PASSWORD} -c "CREATE USER ${LAKEHOUSE_USER} WITH PASSWORD '${LAKEHOUSE_PASS}';"
psql -h postgres -p 5432 -U airflow -d airflow -W ${POSTGRES_PASSWORD} -c "GRANT ALL PRIVILEGES ON DATABASE ${LAKEHOUSE_DB} TO ${LAKEHOUSE_USER};"