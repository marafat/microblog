# SQLAlchamy Notes

After setting up flask-sqlalchemy with your flask app, here are few notes on defining model classes and interacting with them.

##### Define a model class
```python
  # in app/models.py

from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
  ```
   1. model classes inherit from `db.Model`
   2. add columns using `db.Column`, [here](http://docs.sqlalchemy.org/en/latest/core/metadata.html?highlight=column#sqlalchemy.schema.Column) you can find all accepted arguments.
   3. column data types is indicated using an instance which subclasses [TypeEngine](http://docs.sqlalchemy.org/en/latest/core/type_api.html#sqlalchemy.types.TypeEngine). If the type does not require any args, the class can be used: ~~`db.Integer()`~~ but `db.Integer`
   4. The `user_id` field was initialized as a foreign key to `user.id`, which means that it references an id value from the users table. In this reference the `user` part is the name of the database table for the model (check note 6 for table naming conventions)
   5. note how the "many" side of a one-to-many relationship is created: The first argument to `db.relationship` is the model class that represents the "many" side of the relationship. This argument can be provided as a string with the class name if the model is defined later in the module. The `backref` argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a `post.author` expression that will return the user given a post. The `lazy` argument defines how the database query for the relationship will be issued
   6. Table names: Flask-SQLAlchemy uses a "snake case" naming conversion for database tables by default. For the User model above, the corresponding table in the database will be named user. For a AddressAndPhone model class, the table would be named address_and_phone. If you prefer to choose your own table names, you can add an attribute named __tablename__ to the model class, set to the desired name as a string.
   7. Multiple changes can be accumulated in a session and once all the changes have been registered you can issue a single `db.session.commit()`, which writes all the changes atomically. If at any time while working on a session there is an error, a call to `db.session.rollback()` will abort the session and remove any changes stored in it. The important thing to remember is that changes are only written to the database when `db.session.commit()` is called.
  **Extra from flask-sqlalchemy docs:**
   1. we never defined a `__init__` method on the User class? That’s because SQLAlchemy adds an implicit constructor to all model classes which accepts keyword arguments for all its columns and relationships
   2. There is no need to add the Post objects to the session. Since the User is part of the session all objects associated with it through relationships will be added too.

##### Add, update and delete
  **Examples**
  1. add a user:
  ```python
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.commit()
  ```

  2. update user
  ```python
user.username = 'mark'
db.session.commit()
  ```


  3. query all users
  ```python
all_users = User.query.all()
  ```

  4. query user by id
  ```python
user_of_id_1 = User.query.get(1)
  ```

  5. once fetched, all relationships are available
  ```python
posts = user_of_id_1.posts
  ```

  6. delete a user (assuming `user_of_id_1` was fetched)
  ```python
db.session.delete(user_of_id_1)
db.session.commit()
  ```

  7. add post
  ```python
user = User.query.get(1)
post = Post(body='my first post!', author=user)
# note how the kwarg name came from the db.relationship defined on User class
  ```


  8. auto-add object graph
  ```python
user = User(username='john', email='john@example.com')
post = Post(body='some post', author=user)

db.session.add(user)
db.session.commit()

# note how we did not need to add the created post explicitly to db.
# alternatively ...
# db.session.add(post)
# db.session.commit()
# will add the user to db.
  ```