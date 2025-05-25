import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# --- Example usage ---
if __name__ == "__main__":
    db_file = "example.db"

    # Setup sample data (for demonstration)
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY,
                          name TEXT NOT NULL,
                          age INTEGER NOT NULL)''')
        cursor.execute("DELETE FROM users")  # Clear old data
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ('Alice', 30),
            ('Bob', 22),
            ('Charlie', 28),
            ('Daisy', 24)
        ])
        conn.commit()

    # Execute the context-managed query
    query = "SELECT * FROM users WHERE age > ?"
    parameter = (25,)

    with ExecuteQuery(db_file, query, parameter) as result:
        for row in result:
            print(row)
