from flask import Flask
from nanopie import FlaskService

from models import User

app = Flask(__name__)
micro_svc = FlaskService(app=app)


@micro_svc.get(name="get_user", rule="/users/<int:uid>")
def get_user(uid):
    return User(uid=uid, first_name="John", last_name="Smith", age=35)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
