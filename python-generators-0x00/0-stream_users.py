import mysql.connector

# MySQL configuration
HOST = "localhost"
USER = "root"
PASSWORD = "your_mysql_password"  # Replace with your MySQL password
DATABASE = "ALX_prodev"

def stream_users():
    """Generator that yields user rows one by one from the user_data table."""
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    # Yield rows one by one using a single loop
    for row in cursor:
        yield row

    cursor.close()
    connection.close()

# Example usage (for testing purposes only)
if __name__ == "__main__":
    for user in stream_users():
        print(user)
