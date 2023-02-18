"""Module for routes for group and group users"""
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.groups.controller import GroupController, GroupUserController
from app.groups.schema import GroupSchemaIn, GroupSchemaOut, GroupWithUsersSchemaOut
from app.users.controller import JWTBearer, extract_user_id_from_token

group_router = APIRouter(prefix="/api/groups", tags=["Groups"])


@group_router.get("/get-all-groups", response_model=list[GroupSchemaOut])
def get_all_groups():
    return GroupController.get_all()


@group_router.get("/get-all-groups-with-members", response_model=list[GroupWithUsersSchemaOut])
def get_all_groups_with_members():
    return GroupUserController.get_all_joined()


@group_router.post("/create-group", response_model=GroupSchemaOut, dependencies=[Depends(JWTBearer("classic_user"))])
def create_group(request: Request, group: GroupSchemaIn):
    user_id = extract_user_id_from_token(request)
    return GroupController.add_group(group_name=group.group_name, group_owner_id=user_id,
                                     description=group.description)


@group_router.post("/join-group/{group_name}", response_model=GroupWithUsersSchemaOut,
                   dependencies=[Depends(JWTBearer("classic_user"))])
def join_group(request: Request, group_name: str):
    user_id = extract_user_id_from_token(request)
    return GroupUserController.add_group_user(group_name=group_name, user_id=user_id)


@group_router.put("/change-group-name/", response_model=GroupSchemaOut, dependencies=[Depends(JWTBearer("classic_user"))])
def change_group_name(request: Request, group_name: str, new_name: str):
    user_id = extract_user_id_from_token(request)
    return GroupController.change_group_name(group_name=group_name, new_name=new_name, user_id=user_id)


@group_router.delete("/delete-group-by-name/{group_name}", dependencies=[Depends(JWTBearer("super_user"))])
def delete_group_by_name(group_name: str):
    return GroupController.delete_group_by_name(group_name=group_name)
