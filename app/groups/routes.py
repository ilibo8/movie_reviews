"""Module for routes for group and group users"""
from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.groups.controller import GroupController
from app.groups.schema import GroupSchema, GroupSchemaIn
from app.users.controller import JWTBearer
from app.users.service import decodeJWT

group_router = APIRouter(prefix="/api/groups", tags=["Groups"])


@group_router.get("/get-all-groups", response_model=list[GroupSchema])
def get_all_groups():
    return GroupController.get_all()


@group_router.post("/add-group", response_model=GroupSchema, dependencies=[Depends(JWTBearer("classic_user"))])
def add_group(request: Request, group: GroupSchemaIn):
    bearer = request.headers["authorization"]
    token = bearer.split()[1]
    decoded = decodeJWT(token)
    user_id = decoded["user_id"]
    return GroupController.add_group(group_name=group.group_name, group_owner_id=user_id,
                                     description=group.description)


@group_router.delete("/delete-group-by-id/{group_id}")
def delete_group_by_id(group_id: int):
    return GroupController.delete_group_by_id(group_id)
