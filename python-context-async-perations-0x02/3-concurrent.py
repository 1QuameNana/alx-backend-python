import aiosqlite
import asyncio

DB_FILE = "example_async.db"

async def async_setup_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        await db.execute("DELETE FROM users")  # Clear old data for demo
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
        return users

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        older_users = await cursor.fetchall()
        return older_users

async def fetch_concurrently():
    await async_setup_db()  # Setup demo data
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All Users:")
    for user in all_users:
        print(user)
    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)
