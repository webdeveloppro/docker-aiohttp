import asyncio
import logging
import uvloop
import asyncpg

from aiohttp import web

from app.config import CONFIG


async def db_connection(loop, config={}):

    return await asyncpg.connect(
        **config,
        loop=loop
    )


async def on_cleanup(app):
    # await app.db_pool.release(app.db)
    # await app.db_pool.terminate()
    await app.db.close()


async def start_web_app(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    app.conf = CONFIG

    app.db = await db_connection(loop, CONFIG['postgres'])
    app.on_cleanup.append(on_cleanup)

    from app.routes import setup_routes
    setup_routes(app)

    return app, CONFIG['host'], CONFIG['port']


def get_loop():
    logging.basicConfig()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    return loop


def main():
    loop = get_loop()
    app, host, port = loop.run_until_complete(start_web_app(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
