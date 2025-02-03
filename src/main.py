import uvicorn
from fastapi import FastAPI
import os

from backbone.base_class import Base
from backbone.base_entrypoints import router as generic_router
from project_orm import BIND


if False:
    Base.metadata.create_all(BIND)

app = FastAPI()


@app.get("/")
def main_route():
    return {"msg": "api is running"}


app.include_router(generic_router)


if __name__ == "__main__":
    if os.getenv("IS_DOCKER") == "FALSE":
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=80)
