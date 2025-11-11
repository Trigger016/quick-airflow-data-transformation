# M+ Software: Data Engineer (Python) - Airflow Assignment
A minimal local data stack to demo a simple pipeline: ingest a CSV from `MinIO`, load/transform with `DuckDB`, orchestrate everything with `Airflow` and save tables to `Postgres`. Images captured of [tables](http://github.com/Trigger016/quick-airflow-data-transformation/tree/main/docs)

## Essentials
- run this to create several folders for airflow data persist.
```bash
mkdir -p airflow_data/config airflow_data/logs airflow_data/plugins;
```
- it is advisable to manually create different database from the one created by postgres (db `airflow`)
```sql
CREATE DATABASE <database>;
CREATE USER <username> WITH PASSWORD '<password>' ;
GRANT ALL PRIVILEGES ON DATABASE <database> TO <username>;
```

## Pipelines
1) File Check
- A task list objects from specific path in MinIO bucket to get all the `.csv` names.
- The retrieved filename is compared to existing list file (`filename.json`) to check wether the file has been injected before.

2) Load & Transform
- A task queries MinIO (S3 API) and loads objects using DuckDB.
- The file loaded separated between `clean` and `bad` tables. 
- `clean` table then transform & pivoted to be inserted to the target table(`billing`). 

4) Output
- Tables `clean`, `bad` and `target` then saved into postgres using DuckDB

## MinIO notes
- docker `init` profile will create two default buckets to store query and csv files in `data` folder inside the container

## Volumes and persistence
- Airflow metadata persists in postgres
- Postgres data persists in docker volume
- MinIO data persists in docker volume

## Common commands
- Start: docker compose up -d (if first time start use `--profile init`)
- Stop: docker compose down
- View logs: docker compose logs -f airflow-webserver
- Reset stack (danger): docker compose down -v (removes volumes)

## Acknowledgements
- Apache Airflow for orchestration
- DuckDB for data transformations
- Postgres for data storage (lakehouse)
- MinIO for S3-compatible object storage
