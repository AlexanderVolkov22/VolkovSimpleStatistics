from aiogram.utils.json import json
from aiohttp import web

import modules


async def api_get_me(request):
    token = request.match_info['token']
    resp = await modules.getinfo(token)
    resp = str(resp)
    if resp == "Wrong Token!":
        resp_obj = {'status': resp}
        return web.Response(text=json.dumps(resp_obj))
    else:
        resp_obj = {'status': 'ok', 'botname': resp}
        return web.Response(text=json.dumps(resp_obj))


async def register_statistics(request):
    token = request.match_info['token']
    resp = await modules.chktoken(token)
    if resp == "Wrong Token!":
        resp_obj = {'status': resp}
        return web.Response(text=json.dumps(resp_obj))
    else:
        text = request.match_info['text']
        await modules.resp_register(text, token)




if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/{token}/get_me', api_get_me)])
    app.add_routes([web.get('/{token}/send/{text}', register_statistics)])
    web.run_app(app, host="0.0.0.0")
