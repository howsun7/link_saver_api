from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from passlib.apps import custom_app_context as ca_context


db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))
    curriculums = db.relationship('Curriculum', backref='creator', lazy='dynamic')

    def hash_password(self, password):
        self.password = ca_context.encrypt(password)

    def verify_password(self, password):
        return ca_context.verify(password, self.password)

@dataclass
class Curriculum(db.Model):

    __tablename__ = 'curriculums'

    id: int
    name: str
    creater_id: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    creater_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    topics = db.relationship('Topic', backref='curriculum', lazy='dynamic')

@dataclass
class Topic(db.Model):

    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    curriculum_id = db.Column(db.Integer, db.ForeignKey("curriculums.id"))

