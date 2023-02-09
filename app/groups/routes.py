from fastapi import APIRouter
from app.groups.controller import GroupController
from app.groups.schema import GroupSchema, GroupSchemaIn

group_router = APIRouter(prefix="/api/groups", tags=["Groups"])


@group_router.get("/get-all-groups", response_model=list[GroupSchema])
def get_all_groups():
    return GroupController.get_all()


@group_router.post("/add-new-group", response_model=GroupSchema)
def add_new_group(name: str, owner_user_name: str, description: str):
    return GroupController.add_group(name, owner_user_name, description)


@group_router.delete("/delete-group-by-id/{group_id}")
def delete_group_by_id(group_id: int):
    return GroupController.delete_group_by_id(group_id)
