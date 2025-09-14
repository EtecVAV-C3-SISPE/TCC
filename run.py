from flask import Flask
from configuration import configure_all

app = Flask(__name__)

app.secret_key = "MartinLegal565"

configure_all(app)

app.run(debug=True)
