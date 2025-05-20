import mysql.connector

# MySQL configuration
HOST = "localhost"
USER = "root"
PASSWORD = "your_mysql_password"  # Replace with your actual MySQL password
DATABASE = "ALX_prodev"

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # Loop 1
        yield age

    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculates and prints the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

# Run the script
if __name__ == "__main__":
    calculate_average_age()
