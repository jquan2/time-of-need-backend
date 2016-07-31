CREATE TABLE users_locations (
	user_id INTEGER, 
	location_id INTEGER, 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(location_id) REFERENCES location (id)
);

