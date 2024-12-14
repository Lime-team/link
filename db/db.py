import aiomysql
from config_reader import config


async def create(loop):
    conn = await aiomysql.connect(host=config.mysql_host.get_secret_value(),
                                  user=config.mysql_user.get_secret_value(),
                                  password=config.mysql_password.get_secret_value(),
                                  db=config.mysql_db_name.get_secret_value(),
                                  loop=loop)

    async with conn.cursor() as cur:
        await cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INT, 
                            description TEXT,
                            icon TEXT,
                            PRIMARY KEY (id))""")
        await conn.commit()

    conn.close()


async def get(table, column, where_what, is_what, loop):
    conn = await aiomysql.connect(host=config.mysql_host.get_secret_value(),
                                  user=config.mysql_user.get_secret_value(),
                                  password=config.mysql_password.get_secret_value(),
                                  db=config.mysql_db_name.get_secret_value(),
                                  loop=loop)

    cur = await conn.cursor()

    await cur.execute(f"SELECT {column} FROM {table} WHERE {where_what} = %s", (is_what, ))

    r = await cur.fetchall()

    await cur.close()

    conn.close()

    return r


async def set_user(table, tg_id, d, i, loop):
    conn = await aiomysql.connect(host=config.mysql_host.get_secret_value(),
                                  user=config.mysql_user.get_secret_value(),
                                  password=config.mysql_password.get_secret_value(),
                                  db=config.mysql_db_name.get_secret_value(),
                                  loop=loop)

    async with conn.cursor() as cur:
        await cur.execute(f"INSERT INTO {table} (id, description, icon) VALUES (%s, %s, %s)", (tg_id, d, i))
        await conn.commit()

    conn.close()
