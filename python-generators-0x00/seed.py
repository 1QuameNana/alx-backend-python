import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# MySQL configuration
HOST = "localhost"
USER = "root"
PASSWORD = "your_mysql_password"  # Change to your actual MySQL root password
DATABASE = "ALX_prodev"

def connect_db():
    """Connect to the MySQL server (without selecting a database)."""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        print("Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        print(f"Database '{DATABASE}' ensured.")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        print(f"Connected to database '{DATABASE}'.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def create_table(connection):
    """Create the user_data table with required fields."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX(email)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table 'user_data' ensured.")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert user data into the database if email does not already exist."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    SELECT %s, %s, %s, %s
    FROM DUAL
    WHERE NOT EXISTS (
        SELECT 1 FROM user_data WHERE email = %s
    )
    """
    try:
        for row in data:
            uid = str(uuid.uuid4())
            cursor.execute(insert_query, (uid, row['name'], row['email'], row['age'], row['email']))
        connection.commit()
        print(f"{cursor.rowcount} new records inserted.")
    finally:
        cursor.close()

def load_csv_data(csv_file):
    """Load user data from a CSV file."""
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

if __name__ == "__main__":
    # Step 1: Connect and create database
    base_conn = connect_db()
    create_database(base_conn)
    base_conn.close()

    # Step 2: Connect to ALX_prodev
    db_conn = connect_to_prodev()
    create_table(db_conn)

    # Step 3: Load and insert data
    sample_data = load_csv_data("user_data.csv")
    insert_data(db_conn, sample_data)

    db_conn.close()
    print("Seeding complete.")
