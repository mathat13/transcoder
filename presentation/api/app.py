from fastapi import FastAPI

from presentation.api.exception_handlers.register_exception_handlers import register_exception_handlers

from presentation.api.routers import jobs_router

def create_app() ->FastAPI:
    app = FastAPI()

    register_exception_handlers(app=app)
    app.include_router(jobs_router)

    return app