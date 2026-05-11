from fastapi import FastAPI

from presentation.api.setup.register_exception_handlers import register_exception_handlers
from presentation.api.setup.include_routers import include_routers

def create_app() ->FastAPI:
    app = FastAPI()

    register_exception_handlers(app=app)
    include_routers(app=app)

    return app