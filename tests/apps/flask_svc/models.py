from nanopie import IntField, StringField, Model


class User(Model):
    uid = IntField(required=True)
    first_name = StringField(min_length=1, required=True)
    last_name = StringField(min_length=1, required=True)
    age = IntField(minimum=0, maximum=150, required=True)
