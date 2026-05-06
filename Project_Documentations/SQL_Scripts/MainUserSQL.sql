CREATE DATABASE erp_db;

use database erp_db;

CREATE USER admin_erp_db WITH PASSWORD 'abcdef';

ALTER ROLE admin_erp_db SET client_encoding TO 'utf8';

ALTER ROLE admin_erp_db SET default_transaction_isolation TO 'read committed';

ALTER ROLE admin_erp_db SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE erp_db TO admin_erp_db;

GRANT ALL ON SCHEMA public TO admin_erp_db;

ALTER SCHEMA public OWNER TO admin_erp_db;

