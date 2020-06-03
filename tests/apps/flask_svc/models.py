from nanopie import ArrayField, IntField, ObjectField, StringField, Model


class User(Model):
    uid = IntField()
    first_name = StringField(min_length=1, required=True)
    last_name = StringField(min_length=1, required=True)
    age = IntField(minimum=0, maximum=150, required=True)


class UserToPatch(Model):
    first_name = StringField(min_length=1)
    last_name = StringField(min_length=1)
    age = IntField(minimum=0, maximum=150)


class UpdateUserRequest(Model):
    user = ObjectField(model=UserToPatch, required=True)
    masks = ArrayField(item_field=StringField(), min_items=1, required=True)


class ListUsersQueryArgs(Model):
    page_size = IntField(minimum=10, maximum=50, default=20)
    page_token = StringField()


class VerifyUserHeaders(Model):
    test = StringField()
    another_test = IntField(minimum=2, maximum=5)
