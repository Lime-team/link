import asyncio
import db.db as d


async def a():
    loop = asyncio.get_event_loop()
    await d.create(loop)


asyncio.run(a())
