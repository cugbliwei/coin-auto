from aiohttp import web
import json


routes = web.RouteTableDef()


@routes.get('/health')
async def hello(request):
    return web.Response(text="health")


@routes.post('/coin/predict/ascend')
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
    app = web.Application()
    app.router.add_static('/', path='./frontend/dist/', name='html')
    app.router.add_routes(routes)
    web.run_app(app, port='7998')


if __name__ == '__main__':
    run()
