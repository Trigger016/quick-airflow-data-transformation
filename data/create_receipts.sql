USE postgres_db;
CREATE TABLE IF NOT EXISTS refined.clean_receipts
(
    number varchar,
    date date,
    client_code varchar,
    amount int,
    client_type varchar,
    ingested_date date,
    filename varchar
);

CREATE TABLE IF NOT EXISTS refined.bad_receipts
(
    number varchar,
    date date,
    client_code varchar,
    amount int,
    client_type varchar,
    ingested_date date,
    filename varchar
);

CREATE TABLE IF NOT EXISTS marts.billing
(
    date date,
    client_code varchar,
    stt int,
    debit int,
    credit int
);