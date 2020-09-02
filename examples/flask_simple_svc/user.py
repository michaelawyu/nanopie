from nanopie import Model, IntField, StringField


class User(Model):
    name = StringField(max_length=20, min_length=1, pattern="[a-zA-Z]*")
    age = IntField(maximum=100, minimum=0)
