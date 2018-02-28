Exercising the [Mega-flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
The following notes is a quick summary for future reference. I was not particularly interesting in serving client UI from the server, so these are linked directly to the original post.
## Table of Contents:
 * [Chapter 01](##chapter-01): scaffold and run bare bone app.
 * Chapter 02: covers flask html templates rendering and inheritance. [original post](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)
 * [Chapter 03](##chapter-03): web forms, add configurations to a flask app.
 * [Chapter 04](##chapter-04) : databases.

## Chapter 1
This chapter starts from scratch making sure that python 3.4 or higher is installed on the machine.

**Summary:**
 * run `$ python3` from command line
 * `$ mkdir microblog && cd microblog`
 * `$ python3 -m venv venv` (for earlier than 3.4 [virtualenv](https://virtualenv.pypa.io/en/stable/), then `$ viraulenv evn`
 * `$ source venv/bin/activate`
 _(when venv is active, python interpreter is invoked with `python` not `python3`)_
 _(opening the project in PyCharm after this point should be fine. venv will be set as the Project Interpreter automatically)_
 * `(venv) $ pip install flask`
 * create `app` package to serve the app: `(venv) $ mkdir app && cd app`
 * add the `__init__.py`:
 ``` python
 # app/__init__.py

 form flask import Flask

 app = Flask(__name__)

 from app import routes   # added at the end to avoid circular import. (routes.py will import app)
 ```
 * add `routes.py` inside the `app` package. It will hold View functions.
 ``` python
 #app/routes.py: Home page route

 from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
 ```
 * To complete the application, you need to have a Python script at the top-level that defines the Flask application instance. We will call it `microblog.py`:
 ``` python
 # microblog.py

 from app import app
 ```
 * project structure should look like:
 ```
 microblog/
  venv/
  app/
    __init__.py
    routes.py
  microblog.py
 ```

#### Running the app
 * set env var `FLASK_APP` and call `flask run`:
 ``` shell
 (venv) $ export FLASK_APP=microblog.py
 (venv) $ flask run
 ```

## Chapter 03
**Highlights to remember**
 * Using a top-level module `config.py` to handle configurations by defining a class `Config` that holds on to some class variables. This approach is extensible by subclassing `Config`. _(remember to add the config to the flask app after creating its instance by calling `app.config.from_object(Config)`)_
 * security tip: protect against [Cross-Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery) CSRF (pronounced "seasurf"): The package used to handle web forms `Flask-WTF` offers an automatic protection (token generation and inclusion) given two pre-requisites:
   * Having a `SECRET_KEY` item in the app's config
   * adding ` {{ form.hidden_tag() }}` to the html template and inside the container `<form>` tag.
 * Some helpfull methods from flask like:
   * `flash()` which queues a string to flashed msgs. Flash messages are retrieved by calling `get_flashed_messages()`. After this call returns, messages are de-queued and will not be returned on subsequent calls. Usually `get_flashed_messages()` is called within the base html template which gives a global rendering of flash messages.
   * `redirect('path')`
   * `url_for('login')` returns the path associated with the View function named `login`

## Chapter 04
  * Flask does not support databases natively, it is intentionally not opinionated in this area.
  * The search should be for a db in python, that also offers a flask extension.
  * [SQLAlchemy](http://www.sqlalchemy.org/) is an ORM with a flask extension: [Flask-SQLAlchemy](http://packages.python.org/Flask-SQLAlchemy)
  * SQLAlchemy supports a long list of database engines, including MySQL, PostgreSQL, and SQLite.
  * [Alembic](https://bitbucket.org/zzzeek/alembic) , is a database migration tool for SQLAlchemy.
  * [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate) is a flask extension that provides a small wrapper around alembic.

#### Getting started with Flask-Alchemy
##### Add
``` shell
(venv) $ pip install flask-sqlalchemy
```

##### Configure
The extension looks for the following variables in the app's configurations:
  * `SQLALCHEMY_DATABASE_URI` should hold the location to the db.
  * `SQLALCHEMY_TRACK_MODIFICATIONS` _(usually set to `False` [more info](http://flask-sqlalchemy.pocoo.org/2.3/config/) )_
  * create `db` and `migrate` instances in app's package:
  ``` python
  # in app/__init.py__
  ...
  app = Flask(__name__)
  ...
  db = SQLAlchemy(app)
  migrate = Migrate(app, db)
  ```
  _(Note the pattern in initializing flask extensions. Passing the flask app instance to a constructor)_

##### Write database model classes
  * create a new module under `app/` and call it: `models`. This SHOULD be imported in `app/__init__.py` _(by the end of file, just like `routes`)_
  * define some db model classes
  * for more info on defining model classes and interacting with them check out the [SQLAlchemy_notes](SQLAlchemy_notes.md) page.


#### Getting started with Flask-Migrate
Again, Flask-Migrate is a small wrapper around Almebic
##### Add
```shell
(venv) $ pip install flask-migrate
```

##### Initialize Alembic
Alembic requires a directory to store all migration scripts, plus some additional files for its configurations and for creating new migrations.
```shell
(venv) $ export FLASK_APP=microblog.py  # if needed
(venv) $ flask db init
```
This will create a new directory in the project's root called `migrations` with the structure:
```
microblog/
  ...
  migrations/
    version/        # a directory where all migration scripts reside
    alembic.ini
    env.py
    README
    script.py.mako  # a template file used to create new migration scripts
```

Migrations files are python modules. A migration can be expressed using Alembic and SqlAlchemy classes. Alternatively, Alembic provides means to write the SQL code manually.

##### Auto-generate DDL from model classes
Alembic can auto generate the migration files from model classes. For example: at this point of the tutorial, running the following will generate the script that _eventually_ defines the DDL for the users table:
```shell
(venv) $ flask db migrate -m "users table"
```
this will be the output:
```python
# in migrations/versions/8635f4295237_users_table.py
"""users table

Revision ID: 8635f4295237
Revises:
Create Date: 2018-02-27 19:13:11.641464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8635f4295237'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###

```


##### Applying migrations
Each migration version has an auto-generated revision code. Alembic keeps track of the last applied revision. After adding a new revision, it must be applied
```shell
(venv) $ flask db upgrade
```


#### flask shell
you can add the following to `microblog.py` so that when `flask shell` is executed, and interpreter will be loaded with some pre-defined imports
```python
# in microblog.py

...
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
```
