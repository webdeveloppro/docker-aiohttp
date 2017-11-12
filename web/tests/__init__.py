import json
import mock

from app import start_web_app

from aiohttp.test_utils import unittest_run_loop
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.test_utils import make_mocked_request


class HelloAioTest(AioHTTPTestCase):
    url = '/'

    async def get_application(self):
        """Override the get_app method to return your application.
        """
        # it's important to use the loop passed here.
        app, host, port = await start_web_app(self.loop)
        self.mocked_request = make_mocked_request(
            'GET',
            '/',
            app=app,
        )

        return app

    async def request(self, url, method, data={}, headers={}):

        # Do Not share headers and data between tests
        headers_copy = headers.copy()
        data_copy = json.dumps(data)

        headers_copy['content-type'] = headers.get('content-type', 'application/json')
        resp = await self.client.request(method, url, headers=headers_copy, data=data_copy)

        if resp.headers.get('content-type').count('json') > 0:
            jsn = await resp.json()
            return resp.status, jsn or {}
        else:
            return resp.status, await resp.text()

    @unittest_run_loop
    async def test_create(self):
        with mock.patch('asyncpg.connection.Connection.fetchval') as mockConnection:
            FIXTURE = {'text': 'Text test'}

            async def fetchval(query, *params):
                assert query == "insert into item(text) values($1) RETURNING id"
                assert params == ('Text test',)
                return 1
            mockConnection.side_effect = fetchval

            status, data = await self.request(
                self.url,
                'POST',
                FIXTURE,
            )
            assert status == 201

    @unittest_run_loop
    async def test_view(self):
        with mock.patch('asyncpg.connection.Connection.fetch') as mockConnection:
            FIXTURE = [{'id': 1, 'text': 'new todo', 'date_posted': '2017-10-10 10:10'}]

            async def fetch(query, *args, timeout=None) -> list:
                assert query == "SELECT * FROM item"
                assert args == ()
                return FIXTURE
            mockConnection.side_effect = fetch

            status, data = await self.request(
                self.url,
                'GET',
            )
            assert status == 200
            assert data == FIXTURE
