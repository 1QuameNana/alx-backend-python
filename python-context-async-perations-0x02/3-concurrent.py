import aiosqlite
import asyncio

DB_FILE = "example_async.db"

async def async_setup_db():
    """Setup sample users table and data (only once)."""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        await db.execute("DELETE FROM users")  # Clear for demo
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 42),
            ("Charlie", 25),
            ("Diana", 55),
            ("Eve", 19)
        ])
        await db.commit()

async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        print("All Users:")
        for user in users:
            print(user)

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        older_users = await cursor.fetchall()
        print("\nUsers Older Than 40:")
        for user in older_users:
            print(user)

async def fetch_concurrently():
    await async_setup_db()  # Optional: Only for demo setup
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
