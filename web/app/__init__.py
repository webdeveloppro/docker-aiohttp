import asyncio
import aiohttp_jinja2
import logging
import uvloop
import jinja2

from aiohttp import web
from app import sql
from app.config import CONFIG


async def on_cleanup(app):
    app.redis.close()
    await app.redis.wait_closed()
    await app.db_pool.close()


async def start_web_app(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    app.conf = CONFIG

    app.db_pool = await sql.pool_connection(loop, CONFIG['postgres'])
    app.redis = await sql.redis_connection(loop, CONFIG['redis'])
    app.on_cleanup.append(on_cleanup)

    from app.routes import setup_routes
    setup_routes(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(CONFIG['template_dir']))

    return app, CONFIG['host'], CONFIG['port']


def get_loop():
    logging.basicConfig()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    return loop
