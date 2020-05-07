import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app_settings = os.getenv("APP_SETTINGS", "src.config.DevConfig")
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from src.routers import auth_blueprint

app.register_blueprint(auth_blueprint)
