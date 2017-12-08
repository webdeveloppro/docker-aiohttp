import datetime
import json
import traceback

import aiohttp_jinja2
from aiohttp import web
from functools import partial

from app.sql import SQL
from app.schemas import ItemSchema


# JSON serialization tuning
def fix_json(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError


date_dump = partial(json.dumps, indent=None, default=fix_json)


class ItemSQLView(web.View):

    def __init__(self, request):
        self.sql = SQL(request.app)
        super().__init__(request)


class ListView(ItemSQLView):

    async def get(self):
        query = "SELECT * FROM item"
        todo_list = []
        data = await self.sql.execute(query, [], 'fetch')
        for record in data:
            todo_list.append(dict(record))

        counter = await self.request.app.redis.incr('counter')
        context = {
            'items': todo_list,
            'counter': counter
        }

        response = aiohttp_jinja2.render_template(
            'home.html',
            self.request,
            context
        )
        return response


class CreateView(ItemSQLView):

    schema = ItemSchema

    async def perform_create(self, params):
        query = 'insert into {}({}) values({}) RETURNING id'.format(
            'item',
            ','.join(params.keys()),
            ','.join(['$%d' % (x+1) for x in range(0, params.__len__())]),
        )

        result = await self.sql.execute(query, params.values(), 'fetchval')
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

        return web.json_response(text="{}", status=201)
