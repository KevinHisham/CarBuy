from ariadne import QueryType, MutationType
from database import (
    get_all_users, get_user_by_id, get_user_by_email,
    create_user, update_user, delete_user
)

query = QueryType()
mutation = MutationType()

def user_to_dict(user_row):
    """Convert database row to dictionary"""
    if not user_row:
        return None
    
    return {
        "id": str(user_row["id"]),
        "name": user_row["name"],
        "email": user_row["email"],
        "phone": user_row["phone"],
        "address": user_row["address"],
        "createdAt": user_row["created_at"],
        "updatedAt": user_row["updated_at"]
    }

@query.field("users")
def resolve_users(*_):
    users = get_all_users()
    return [user_to_dict(user) for user in users]

@query.field("user")
def resolve_user(_, info, id):
    user = get_user_by_id(int(id))
    return user_to_dict(user)

@query.field("userByEmail")
def resolve_user_by_email(_, info, email):
    user = get_user_by_email(email)
    return user_to_dict(user)

@mutation.field("createUser")
def resolve_create_user(_, info, input):
    try:
        user = create_user(
            name=input["name"],
            email=input["email"],
            phone=input.get("phone"),
            address=input.get("address")
        )
        return user_to_dict(user)
    except Exception as e:
        raise Exception(f"Failed to create user: {str(e)}")

@mutation.field("updateUser")
def resolve_update_user(_, info, id, input):
    try:
        user = update_user(int(id), **input)
        if not user:
            raise Exception("User not found")
        return user_to_dict(user)
    except Exception as e:
        raise Exception(f"Failed to update user: {str(e)}")

@mutation.field("deleteUser")
def resolve_delete_user(_, info, id):
    try:
        return delete_user(int(id))
    except Exception as e:
        raise Exception(f"Failed to delete user: {str(e)}")