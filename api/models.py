from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from passlib.apps import custom_app_context as ca_context
# from .app import db

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        self.password = ca_context.encrypt(password)

    def verify_password(self, password):
        return ca_context.verify(password, self.password)


# class Curriculums(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))
#     creater_id = db.Column(db.Integer, db.ForeignKey(""))

# class Topics(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))

