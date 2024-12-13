import asyncio

import aiomysql
from config_reader import config

loop = asyncio.get_event_loop()


async def create():
    conn = await aiomysql.connect(host=config.mysql_host.get_secret_value(),
                                  user=config.mysql_user.get_secret_value(),
                                  password=config.mysql_password.get_secret_value(),
                                  db=config.mysql_db_name.get_secret_value(),
                                  loop=loop)

    async with conn.cursor() as cur:
        await cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT, 
                            description TEXT,
                            icon TEXT,
                            PRIMARY KEY (id))""")
        await conn.commit()

    conn.close()


async def get(column, what, is_what):
    conn = await aiomysql.connect(host=config.mysql_host.get_secret_value(),
                                  user=config.mysql_user.get_secret_value(),
                                  password=config.mysql_password.get_secret_value(),
                                  db=config.mysql_db_name.get_secret_value(),
                                  loop=loop)

    cur = await conn.cursor()

    await cur.execute(f"SELECT %s FROM users WHERE id = %s", (column, is_what))

    r = await cur.fetchall()

    await cur.close()

    conn.close()

    return r


async def set(d, i):
    conn = await aiomysql.connect(host=config.mysql_host.get_secret_value(),
                                  user=config.mysql_user.get_secret_value(),
                                  password=config.mysql_password.get_secret_value(),
                                  db=config.mysql_db_name.get_secret_value(),
                                  loop=loop)

    async with conn.cursor() as cur:
        await cur.execute(f"INSERT INTO users (description, icon) VALUES (%s, %s)", (d, i))
        await conn.commit()

    conn.close()
