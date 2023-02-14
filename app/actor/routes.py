from fastapi import APIRouter
from app.actor.controller import ActorController
from app.actor.schema import ActorSchema, ActorSchemaIn

actor_router = APIRouter(prefix="/api/movies/actors", tags=["Movies - Actors"])


@actor_router.get("/get-all", response_model=list[ActorSchema])
def get_all_actors():
    return ActorController.get_all_actors()


@actor_router.get("/get-all/names", response_model=list[str])
def get_all_actors_only_full_names():
    return ActorController.get_all_actors_names()


@actor_router.get("/get-actors-by-id/{id}", response_model=ActorSchema)
def get_actor_by_id(id: int):
    return ActorController.get_actor_by_id(id)


@actor_router.get("/get-actors-by/name", response_model=list[ActorSchema])
def find_actors_by_name(name: str):
    return ActorController.find_actor_by_name(name)


@actor_router.get("/get-actors-by/last_name", response_model=list[ActorSchema])
def find_actors_by_last_name(last_name: str):
    return ActorController.find_actor_by_last_name(last_name)


@actor_router.post("/add-actor", response_model=ActorSchema)
def add_actor(actor: ActorSchemaIn):
    return ActorController.add_actor(actor.full_name, actor.nationality)


@actor_router.put("/change/full-name/{actor_id}", response_model=ActorSchema)
def change_actor_full_name(actor_id: int, full_name: str):
    return ActorController.change_actor_full_name(actor_id, full_name)


@actor_router.delete("/delete-actor-by-id/{actor_id}")
def delete_actor_by_id(actor_id: int):
    return ActorController.delete_actor_by_id(actor_id)
