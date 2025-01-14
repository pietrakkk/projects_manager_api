import logging
from http import HTTPStatus

from endpoints.projects.api import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

app = FastAPI(title="ProjectManager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", status_code=HTTPStatus.OK)
async def root():
    return {"message": "ProjectManagement API"}


if __name__ == "__main__":
    logging.basicConfig(level=settings.log_level)
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
