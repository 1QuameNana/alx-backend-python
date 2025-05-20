import mysql.connector

# MySQL configuration
HOST = "localhost"
USER = "root"
PASSWORD = "your_mysql_password"  # Replace with your actual MySQL password
DATABASE = "ALX_prodev"

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from the user_data table in batches of `batch_size`.
    """
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    Yields only the users whose age > 25.
    """
    for batch in stream_users_in_batches(batch_size):          # Loop 1
        filtered_users = [user for user in batch if user['age'] > 25]  # Loop 2 (list comp counts as one loop)
        for user in filtered_users:                            # Loop 3
            yield user

# Example usage (for testing)
if __name__ == "__main__":
    for user in batch_processing(2):
        print(user)
