CREATE TABLE registered_user (
	id serial primary key,
	name text not null,
	age integer not null,
	email text not null,
	password text not null,
	location text not null
)
