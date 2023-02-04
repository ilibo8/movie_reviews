from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.genre.exceptions import GenreNotFoundException, NoEntryForGenreException, GenreAlreadyExistsException
from app.genre.service import GenreService


class GenreController:

    @staticmethod
    def add_genre(name: str):
        try:
            genre = GenreService.add_genre(name)
            return genre
        except GenreAlreadyExistsException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_genres():
        try:
            genres = GenreService.get_all_genres()
            return genres
        except NoEntryForGenreException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete(name: str):
        try:
            if GenreService.delete(name):
                return Response(content=f"Genre {name} is deleted", status_code=200)
        except GenreNotFoundException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
