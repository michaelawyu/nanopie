import uuid

from flask import Flask
from nanopie import FlaskService, parsed_request, HTTPMethods, HTTPResponse
from nanopie.misc.errors import ValidationError

if __package__ == None or __package__ == "":
    from models import User, UpdateUserRequest, ListUsersQueryArgs
else:
    from .models import User, UpdateUserRequest, ListUsersQueryArgs

app = Flask(__name__)
micro_svc = FlaskService(app=app)

UID = 74900978634380746928517603352148324307

dummy_storage = [{"uid": UID, "first_name": "John", "last_name": "Smith", "age": 35}]

INVALID_INPUT_RES = HTTPResponse(status_code=400, data="Input is not valid.")
USER_NOT_EXIST_RES = HTTPResponse(status_code=400, data="User does not exist.")

ATTR_NOT_FOUND_FLAG = object()


def find_user_data(uid):
    for i in range(0, len(dummy_storage)):
        if dummy_storage[i].get("uid") == uid:
            user_data = dummy_storage[i]
            return i, user_data

    return None, None


@micro_svc.get(name="get_user", rule="/users/<int:uid>")
def get_user(uid):
    i, user_data = find_user_data(uid)  # pylint: disable=unused-variable
    if user_data == None:
        return USER_NOT_EXIST_RES

    user = User.from_dikt(user_data)

    return user


@micro_svc.create(name="create_user", rule="/users", data_cls=User)
def create_user():
    user = parsed_request.data
    try:
        user.validate()
    except ValidationError:
        return INVALID_INPUT_RES

    uid = uuid.uuid4().int
    user.uid = uid
    dummy_storage.append(user.to_dikt())

    return user


@micro_svc.update(
    name="update_user", rule="/users/<int:uid>", data_cls=UpdateUserRequest
)
def update_user(uid):
    update_user_req = parsed_request.data
    try:
        update_user_req.validate()
    except ValidationError:
        return INVALID_INPUT_RES

    i, user_data = find_user_data(uid)
    if user_data == None:
        return USER_NOT_EXIST_RES

    user = User.from_dikt(user_data)
    new_user = update_user_req.user

    for mask in update_user_req.masks:
        if (
            getattr(user, mask, ATTR_NOT_FOUND_FLAG) != ATTR_NOT_FOUND_FLAG
            and getattr(new_user, mask, ATTR_NOT_FOUND_FLAG) != ATTR_NOT_FOUND_FLAG
        ):
            new_value = getattr(new_user, mask)
            setattr(user, mask, new_value)
        else:
            return INVALID_INPUT_RES

    dummy_storage[i] = user.to_dikt()

    return user


@micro_svc.delete(name="delete_user", rule="/users/<int:uid>")
def delete_user(uid):
    i, user_data = find_user_data(uid)
    if user_data == None:
        return USER_NOT_EXIST_RES

    user = User.from_dikt(user_data)
    del dummy_storage[i]
    return user


@micro_svc.list(name="list_users", rule="/users", query_args_cls=ListUsersQueryArgs)
def list_users():
    list_users_query_args = parsed_request.query_args
    try:
        list_users_query_args.validate()
    except ValidationError:
        return INVALID_INPUT_RES

    page_size = list_users_query_args.page_size

    list_users_res = [
        User.from_dikt(user_data) for user_data in dummy_storage[: page_size + 1]
    ]
    return list_users_res


@micro_svc.custom(
    name="verify_user", rule="/users/<int:uid>", verb="verify", method=HTTPMethods.GET
)
def verify_user(uid):
    i, user_data = find_user_data(uid)  # pylint: disable=unused-variable
    if user_data == None:
        return USER_NOT_EXIST_RES

    user = User.from_dikt(user_data)
    return user


if __name__ == "__main__":
    app.run(port=8080, debug=True)
