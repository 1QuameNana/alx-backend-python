import sqlite3
import functools

#  Decorator that opens and closes DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open DB connection
        try:
            # Call the wrapped function, injecting the connection
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # Ensure the connection is always closed
    return wrapper

#  Use the decorator
@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone() 

#  Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
