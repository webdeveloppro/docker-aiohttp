from aiohttp import web
from app import get_loop, start_web_app


def main():
    loop = get_loop()
    app, host, port = loop.run_until_complete(start_web_app(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
