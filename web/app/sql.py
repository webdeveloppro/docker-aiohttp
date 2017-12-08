import asyncio
import aioredis
import asyncpg


class SQL(object):

    def __init__(self, app):
        self.app = app
        self.conn = None

    async def get_connection(self):
        if self.conn is None:
            attemp = 0
            delay = 0.5
            while attemp != 10:
                try:
                    self.conn = await self.app.db_pool.acquire()
                    return self.conn
                except:
                    await asyncio.sleep(delay)
                    attemp += 1
            raise "Not free sql connections"

    async def execute(self, query, params=[], fetch_method='execute'):
        await self.get_connection()

        try:
            if fetch_method == 'execute':
                result = await self.conn.execute(query, *params)
            elif fetch_method == 'fetch':
                result = await self.conn.fetch(query, *params)
            elif fetch_method == 'fetchrow':
                result = await self.conn.fetchrow(query, *params)
            elif fetch_method == 'fetchval':
                result = await self.conn.fetchval(query, *params)
        finally:
            await self.release()

        return result

    async def release(self):
        if self.conn:
            await self.app.db_pool.release(self.conn)
            self.conn = None


async def pool_connection(loop=None, config=None):

    if config is None:
        from app.config import CONFIG
        config = CONFIG['postgres']

    return await asyncpg.create_pool(
        **config,
        loop=loop,
    )


async def redis_connection(loop=None, config={}):
    return await aioredis.create_redis(
        (config['host'], config['port'],),
        loop=loop
    )
