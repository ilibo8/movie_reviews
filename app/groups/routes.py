"""Module for routes for group and group users"""
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.groups.controller import GroupController, GroupUserController
from app.groups.schema import GroupSchemaIn, GroupSchemaOut, GroupWithUsersSchemaOut, GroupSchema, GroupUserNamesSchema
from app.users.controller import JWTBearer, extract_user_id_from_token

group_router = APIRouter(prefix="/api/groups", tags=["Groups"])
group_superuser_router = APIRouter(prefix="/api/superuser/groups", tags=["superuser - Groups & Recommendations"])


@group_router.get("/get-all-groups", response_model=list[GroupSchemaOut])
def get_all_groups():
    """
    The function returns a list of all the groups in the database.
    """
    return GroupController.get_all_reformatted()


@group_router.get("/get-all-groups-with-members", response_model=list[GroupWithUsersSchemaOut])
def get_all_groups_with_members():
    """
    The function returns a list of all groups that have at least one member.
    """
    return GroupUserController.get_all_joined()


@group_router.get("/your-group-names", response_model=list[str], dependencies=[Depends(JWTBearer("classic_user"))])
def get_your_groups(request: Request):
    """
    The function returns a list of all groups user is part of.
    """
    user_id = extract_user_id_from_token(request)
    return GroupUserController.get_all_groups_having_user_by_user_id(user_id)


@group_router.post("/create-group", response_model=GroupSchemaOut, dependencies=[Depends(JWTBearer("classic_user"))])
def create_group(group: GroupSchemaIn, request: Request):
    """
    The function creates a new group with the given name and description.
    It is called when a user wants to create a new group.
    """
    user_id = extract_user_id_from_token(request)
    return GroupController.add_group(group_name=group.group_name, owner_user_id=user_id,
                                     description=group.description)


@group_router.post("/join-group/{group_name}", response_model=GroupWithUsersSchemaOut,
                   dependencies=[Depends(JWTBearer("classic_user"))])
def join_group(request: Request, group_name: str):
    """
    The function allows a user to join an existing group.
    """
    user_id = extract_user_id_from_token(request)
    return GroupUserController.add_group_user(group_name=group_name, user_id=user_id)


@group_router.put("/change-group-name/", response_model=GroupSchemaOut,
                  dependencies=[Depends(JWTBearer("classic_user"))])
def change_group_name(request: Request, group_name: str, new_name: str):
    """
    The function allows a user to change the name of their group.
    The function checks if the user is an admin of that group and if they are changes the name to new_name.
    """
    user_id = extract_user_id_from_token(request)
    return GroupController.change_group_name(group_name=group_name, new_name=new_name, user_id=user_id)


@group_superuser_router.get("/get-all-groups", response_model=list[GroupSchema],
                            dependencies=[Depends(JWTBearer("super_user"))],)
def get_all_groups():
    """
    Get info about all groups - for superuser.
    """
    return GroupController.get_all()


@group_superuser_router.get("/get-all-group-users", response_model=list[GroupUserNamesSchema],
                            dependencies=[Depends(JWTBearer("super_user"))],)
def get_all_group_users():
    """
    Get info about all groups and their members - for superuser.
    """
    return GroupController.get_all_group_users()


@group_superuser_router.delete("/delete-group-by-id/{group_id}", dependencies=[Depends(JWTBearer("super_user"))])
def delete_group_by_id(group_id: int):
    """
    The function deletes a group from the database.
    """
    return GroupController.delete_group_by_id(group_id=group_id)
