--<keep_data>
CREATE TABLE bookings.airports_data (
	airport_code bpchar(3) NOT NULL,
	airport_name jsonb NOT NULL,
	city jsonb NOT NULL,
	coordinates point NOT NULL,
	timezone varchar NOT NULL,
    load_date date NULL
);