USE postgres_db;

WITH read_source as (
    SELECT 
        number,
        date,
        client_code,
        amount,
        client_type,
        current_date as ingested_date,
        '{pattern}' as filename
    FROM read_csv('s3://data-landing/{pattern}')
    WHERE number IS NOT NULL 
    AND amount IS NOT NULL
    AND date IS NOT NULL
    AND client_code IS NOT NULL 
    AND client_type IS NOT NULL
)
MERGE INTO refined.clean_receipts dst
USING read_source as src
ON src.number = dst.number
WHEN MATCHED AND src.filename > dst.filename THEN
    UPDATE SET 
        date = src.date,
        client_code = src.client_code,
        amount = src.amount,
        client_type = src.client_type,
        ingested_date = src.ingested_date,
        filename = src.filename
WHEN NOT MATCHED THEN
    INSERT (number, date, client_code, amount, client_type, ingested_date, filename)
    VALUES (
       src.number,
       src.date,
       src.client_code,
       src.amount,
       src.client_type,
       src.ingested_date,
       src.filename
    );