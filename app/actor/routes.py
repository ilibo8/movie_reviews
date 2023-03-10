"""Module for routes regarding Actor table."""
from fastapi import APIRouter, Depends
from app.actor.controller import ActorController
from app.actor.schema import ActorSchema, ActorSchemaIn
from app.users.controller import JWTBearer

actor_superuser_router = APIRouter(prefix="/api/superuser/movies/actors", tags=["superuser - Actors & Genre"])


@actor_superuser_router.get("/get-all", response_model=list[ActorSchema],
                            dependencies=[Depends(JWTBearer("super_user"))])
def get_all_actors():
    """
    The function returns a list of all actors in the database.
    """
    return ActorController.get_all_actors()


@actor_superuser_router.get("/get-actors-by/name", response_model=list[ActorSchema],
                            dependencies=[Depends(JWTBearer("super_user"))])
def find_actors_by_name(name: str):
    """
    The function takes a string as an argument and returns a list of actors whose name contains the string.
    """
    return ActorController.find_actor_by_name(name)


@actor_superuser_router.get("/get-actors-by/last_name", response_model=list[ActorSchema],
                            dependencies=[Depends(JWTBearer("super_user"))])
def find_actors_by_last_name(last_name: str):
    """
    The function takes a last name as an argument and returns all actors with that last name.
    """
    return ActorController.find_actor_by_last_name(last_name)


@actor_superuser_router.post("/add-actor", response_model=ActorSchema, dependencies=[Depends(JWTBearer("super_user"))])
def add_actor(actor: ActorSchemaIn):
    """
    The function adds a new actor to the database.
    """
    return ActorController.add_actor(actor.full_name, actor.nationality)


@actor_superuser_router.put("/change/full-name/{actor_id}", response_model=ActorSchema,
                            dependencies=[Depends(JWTBearer("super_user"))])
def change_actor_full_name(actor_id: int, full_name: str):
    """
    The function takes an actor_id and a full_name as arguments.
    It then updates the database to change the full name of that actor to the new one.
    """
    return ActorController.change_actor_full_name(actor_id, full_name)


@actor_superuser_router.delete("/delete-actor-by-id/{actor_id}", dependencies=[Depends(JWTBearer("super_user"))])
def delete_actor_by_id(actor_id: int):
    """
    The function deletes an actor from the database by their ID.
    """
    return ActorController.delete_actor_by_id(actor_id)
