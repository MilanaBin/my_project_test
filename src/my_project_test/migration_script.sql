--<keep_data>
CREATE TABLE bookings.airports_data (
	airport_code bpchar(3) NOT NULL,
	airport_name jsonb NOT NULL,
	city jsonb NOT NULL,
	coordinates point NOT NULL,
	timezone varchar NOT NULL,
	dt date NULL
);

COMMENT ON TABLE bookings.airports_data IS 'Данные об аэропортах, включая код, название, город, координаты и часовой пояс';
COMMENT ON COLUMN bookings.airports_data.airport_code IS 'Код аэропорта (3 символа)';
COMMENT ON COLUMN bookings.airports_data.airport_name IS 'Название аэропорта в формате JSONB, поддерживающее локализацию';
COMMENT ON COLUMN bookings.airports_data.city IS 'Город в формате JSONB, поддерживающий локализацию';
COMMENT ON COLUMN bookings.airports_data.coordinates IS 'Географические координаты аэропорта (точка: долгота и широта)';
COMMENT ON COLUMN bookings.airports_data.timezone IS 'Часовой пояс аэропорта';