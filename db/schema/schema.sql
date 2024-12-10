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