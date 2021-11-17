from aiohttp import web

from app.main import create_app


app = create_app()
config = app.container.config
host = config.app.host()
port = config.app.port()
web.run_app(app, host=host, port=port)
