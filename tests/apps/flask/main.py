from flask import Flask
from nanopie import FlaskService

app = Flask(__name__)
micro_svc = FlaskService(app=app)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
