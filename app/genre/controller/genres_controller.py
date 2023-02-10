from fastapi import HTTPException, Response
from app.genre.exceptions import GenreAlreadyExists, NoEntryForGenre, GenreNotFound
from app.genre.service import GenreService


class GenreController:

    @staticmethod
    def add_genre(name: str):
        try:
            genre = GenreService.add_genre(name)
            return genre
        except GenreAlreadyExists as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_genres():
        try:
            genre_names = []
            genres = GenreService.get_all_genres()
            for genre in genres:
                genre_names.append(genre.name)
            return genre_names
        except NoEntryForGenre as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete(name: str):
        try:
            if GenreService.delete(name):
                return Response(content=f"Genre {name} is deleted", status_code=200)
        except GenreNotFound as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
