 MySQL Seeder for ALX_prodev
This script sets up a MySQL database for an Airbnb-style project by:

Connecting to the MySQL server

Creating a new database called ALX_prodev (if it doesn't exist)

Creating a table user_data with appropriate fields and indexing

Reading user information from a CSV file (user_data.csv)

Inserting new user records into the table, avoiding duplicates based on email

🧩 Table Structure: user_data
Field	Type	Constraints
user_id	UUID (CHAR)	Primary Key, Indexed
name	VARCHAR	Not Null
email	VARCHAR	Not Null, Indexed
age	DECIMAL	Not Null

🧪 Key Functions
connect_db()
Connects to the MySQL server (without selecting a database). Used for creating the initial database.

create_database(connection)
Creates the ALX_prodev database if it doesn't already exist.

connect_to_prodev()
Reconnects to the MySQL server, this time selecting the ALX_prodev database.

create_table(connection)
Creates the user_data table with the following:

UUID primary key (user_id)

Fields: name, email, age

Email is also indexed for performance.

insert_data(connection, data)
Inserts user data into the database only if the email doesn't already exist. Avoids duplicates based on the email field.

load_csv_data(csv_file)
Reads user data from a CSV file and returns it as a list of dictionaries. Expects columns: name, email, age