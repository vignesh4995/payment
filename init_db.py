import asyncio
import asyncpg

DATABASE_URL = "postgresql://user:password@db/postgres"

async def create_database():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('CREATE DATABASE payment_db')
    await conn.close()

asyncio.run(create_database())
