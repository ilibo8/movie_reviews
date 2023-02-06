import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.db.database import engine, Base

from app.actor import actor_router
from app.movie import movie_router
from app.genre import genre_router

Base.metadata.create_all(bind=engine)


def init_app():
    app = FastAPI()
    app.include_router(movie_router)
    app.include_router(actor_router)
    app.include_router(genre_router)
    return app


app = init_app()


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse('/docs')


if __name__ == "__main__":
    uvicorn.run(app)
