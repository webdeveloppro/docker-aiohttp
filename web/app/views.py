import datetime
import json
import traceback

from aiohttp import web
from functools import partial

from .schemas import ItemSchema


# JSON serialization tuning
def fix_json(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError


date_dump = partial(json.dumps, indent=None, default=fix_json)


class ListView(web.View):

    async def get(self):
        query = "SELECT * FROM item"
        todo_list = []
        data = await self.request.app.db.fetch(query)
        for record in data:
            todo_list.append(dict(record))

        return web.json_response(todo_list, dumps=date_dump, status=200)


class CreateView(web.View):

    schema = ItemSchema

    async def perform_create(self, params):
        query = 'insert into {}({}) values({}) RETURNING id'.format(
            'item',
            ','.join(params.keys()),
            ','.join(['$%d' % (x+1) for x in range(0, params.__len__())]),
        )

        result = await self.request.app.db.fetchval(query, *params.values())
        return result

    async def get_schema_data(self, schema=None, partial=False):

        data = await self.request.json()
        if not data:
            raise web.HTTPBadRequest(
                text='Empty data',
                content_type='application/json')
        try:
            schema_result = self.schema().load(data)
        except Exception as e:
            raise web.HTTPBadRequest(
                text=traceback.format_exc(3, 100),
                content_type='application/json')

        if schema_result.errors:
            raise web.HTTPBadRequest(
                text="{}, data: {}".format(
                    json.dumps(schema_result.errors),
                    data
                ),
                content_type='application/json'
            )

        return schema_result

    async def post(self):

        # data schema checking
        schema_result = await self.get_schema_data()

        if schema_result.data.keys().__len__() == 0:
            return web.json_response({'status': 204, 'error': 'No content'}, status=204)

        try:
            await self.perform_create(schema_result.data)
        except Exception as e:
            return web.json_response(e, status=500)

        return web.json_response({"ok": 1}, status=201)
