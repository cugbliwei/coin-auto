from aiohttp import web
import aiohttp_jinja2
import jinja2
import json
import sys


routes = web.RouteTableDef()


@routes.get('/')
async def home(request):
    raise web.HTTPFound('/coin/index')


@routes.get('/coin/index')
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@routes.post('/api/predict/ascend')
async def otc_user_set(request):
    try:
        with open('result.json', 'r') as f:
            data = json.load(f)
        if not data:
            return web.json_response({'status': False, 'data': []})
        else:
            return web.json_response({'status': True, 'data': data})
    except:
        return web.json_response({'status': False, 'data': []})


def run():
    port = '3389'
    if len(sys.argv) > 1:
        port = sys.argv[1]

    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
    app.router.add_static('/static', './static/dist/', name='static')
    app.router.add_routes(routes)
    web.run_app(app, port=port)


if __name__ == '__main__':
    run()
