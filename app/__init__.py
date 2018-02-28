from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# initialize db
db = SQLAlchemy(app)

# initialize migration engine
migrate = Migrate(app, db)

from app import routes, models