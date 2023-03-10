"""Module for running app."""
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.db.database import engine, Base
from app.actor import actor_superuser_router
from app.genre import genre_superuser_router
from app.movie import movie_router, movie_superuser_router
from app.users import login_router, user_router, register_router
from app.groups import group_router, group_superuser_router
from app.recommendations import recommendations_router, recommendations_superuser_router
from app.reviews import reviews_router, reviews_superuser_router


Base.metadata.create_all(bind=engine)


def init_app():
    """
    The init_app function is a helper function that creates the FastAPI app and includes all the routers.
    """
    app = FastAPI(title="Movie reviews")
    app.include_router(login_router)
    app.include_router(register_router)
    app.include_router(movie_router)
    app.include_router(reviews_router)
    app.include_router(group_router)
    app.include_router(recommendations_router)
    app.include_router(user_router)
    app.include_router(movie_superuser_router)
    app.include_router(actor_superuser_router)
    app.include_router(genre_superuser_router)
    app.include_router(recommendations_superuser_router)
    app.include_router(group_superuser_router)
    app.include_router(reviews_superuser_router)
    return app


app = init_app()


@app.get("/", include_in_schema=False)
def redirect():
    """
    The redirect function is used to redirect the user to the documentation page.
    """
    return RedirectResponse('/docs')


if __name__ == "__main__":
    uvicorn.run(app)
