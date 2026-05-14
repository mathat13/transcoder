from fastapi import FastAPI

from presentation.api.setup.definitions.routers import jobs_router

def include_routers(app: FastAPI) -> None:
    app.include_router(jobs_router)