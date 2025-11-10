USE postgres_db;
TRUNCATE TABLE marts.billing;

WITH refined_data AS (
    SELECT 
        number,
        date,
        client_code,
        amount,
        client_type,
        ingested_date,
        filename
    FROM refined.clean_receipts
)
INSERT INTO marts.billing(date, client_code, stt, debit, credit)
SELECT 
    date,
    client_code,
    count(client_code) AS stt,
    sum(CASE
        WHEN client_type = 'C' then amount
        ELSE 0
    END) AS debit,
    sum(CASE
        WHEN client_type = 'V' then amount
        ELSE 0
    END) AS credit,
FROM refined_data
GROUP BY client_code, date
ORDER BY client_code, date
;