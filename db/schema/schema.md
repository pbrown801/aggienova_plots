# Schema
1. supernovae
    - sn_id (PRIMARY KEY)
    - sn_name: text
        - force uniqueness across columns
        - mandatory field
    - redshift: numeric
        - uniqueness not enforced
        - nullable field
    - distance_modulus: numeric
        - uniqueness not enforced
        - nullable field
    - type_id (FOREIGN KEY)
        - uniqueness not enforced
        - nullable field
2. sn_types
    - type_id (PRIMARY KEY)
    - type_name: text
        - force uniqueness across columns
        - mandatory field
3. filters
    - filter_id (PRIMARY KEY)
    - filter_name: text
        - force uniqueness across columns
        - mandatory field
4. light_curves
    - curve_id (PRIMARY KEY)
    - sn_id (FOREIGN KEY)
        - uniqueness not enforced
        - mandatory field
    - filter_id (FOREIGN KEY)
        - uniqueness not enforced
        - mandatory field
    - mjd: numeric
        - uniqueness not enforced
        - mandatory field
    - magnitude: numeric
        - uniqueness not enforced
        - nullable field
    - magnitude_error: numeric
        - uniqueness not enforced
        - nullable field
    - hash: text
        - force uniqueness across columns
        - mandatory field
---
## Create Tables
```sql
CREATE TABLE sn_types (
    type_id SERIAL PRIMARY KEY,
    type_name TEXT UNIQUE NOT NULL
);

CREATE TABLE filters (
    filter_id SERIAL PRIMARY KEY,
    filter_name TEXT UNIQUE NOT NULL
);

CREATE TABLE supernovae (
    sn_id SERIAL PRIMARY KEY,
    sn_name TEXT UNIQUE NOT NULL,
    redshift NUMERIC,
    distance_modulus NUMERIC,
    type_id INT REFERENCES sn_types(type_id) ON DELETE SET NULL
);

CREATE TABLE light_curves (
    curve_id SERIAL PRIMARY KEY,
    sn_id INT NOT NULL REFERENCES supernovae(sn_id) ON DELETE CASCADE,
    filter_id INT NOT NULL REFERENCES filters(filter_id) ON DELETE RESTRICT,
    mjd NUMERIC NOT NULL,
    magnitude NUMERIC,
    magnitude_error NUMERIC,
    hash TEXT UNIQUE NOT NULL
);
```
## Drop All Tables
```sql
DO
$$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
    LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END
$$;
```
supabase password: 5gIyEgLhDRk9kB1L