import mysql.connector

# MySQL configuration
HOST = "localhost"
USER = "root"
PASSWORD = "your_mysql_password"  # Replace with your MySQL password
DATABASE = "ALX_prodev"

def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the user_data table.
    """
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that lazily paginates the user_data table one page at a time.
    Starts at offset 0 and fetches the next page only when needed.
    """
    offset = 0
    while True:  # Only one loop used
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage (for testing)
if __name__ == "__main__":
    for page in lazy_paginate(2):
        print(f"Page:")
        for user in page:
            print(user)
