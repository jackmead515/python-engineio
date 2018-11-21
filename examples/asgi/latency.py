import os
import uvicorn

import engineio
from engineio.async_asgi import create_asgi_app

from app import App

eio = engineio.AsyncServer(async_mode='asgi')
app = create_asgi_app(eio, App({
    '/latency.html': b'text/html',
    '/static/engine.io.js': b'application/javascript',
    '/static/style.css': b'text/css',
}))


async def index(request):
    with open('latency.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@eio.on('message')
async def message(sid, data):
    await eio.send(sid, 'pong', binary=False)


if __name__ == '__main__':
    uvicorn.run(app, '127.0.0.1', 5000)
