Exercising the [Mega-flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## Table of Contents:
 * [Chapter 1](##chapter-1): scaffold and run bare bone app.
 * Chapter 2: covers flask html templates rendering and inheritance. [original post](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)

## Chapter 1:
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
 ``` python3
 # app/__init__.py

 form flask import Flask

 app = Flask(__name__)

 from app import routes   # added at the end to avoid circular import. (routes.py will import app)
 ```
 * add `routes.py` inside the `app` package. It will hold View functions.
 ``` python3
 #app/routes.py: Home page route

 from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
 ```
 * To complete the application, you need to have a Python script at the top-level that defines the Flask application instance. We will call it `microblog.py`:
 ``` python3
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

#### Running the app:
 * set env var `FLASK_APP` and call `flask run`:
 ``` shell
 (venv) $ export FLASK_APP=microblog.py
 (venv) $ flask run
 ```