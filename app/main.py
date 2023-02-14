import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.db.database import engine, Base

from app.actor import actor_router
from app.groups import group_router

from app.movie import movie_router, movie_superuser_router
from app.genre import genre_router
from app.reviews import reviews_router
from app.users.routes import login_router, user_router

Base.metadata.create_all(bind=engine)


def init_app():
    app = FastAPI(title="Movie reviews")
    app.include_router(login_router)
    app.include_router(user_router)
    app.include_router(group_router)
    app.include_router(movie_router)
    app.include_router(reviews_router)
    app.include_router(movie_superuser_router)
    app.include_router(actor_router)
    app.include_router(genre_router)

    return app


app = init_app()


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse('/docs')


if __name__ == "__main__":
    uvicorn.run(app)
