DROP TABLE IF EXISTS item;

CREATE TABLE item (
    id serial PRIMARY KEY,
    text character varying(255) NOT NULL,
    date_posted timestamp with time zone DEFAULT now()
);
