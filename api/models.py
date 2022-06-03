from .app import db

class User(db.Model):

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), index=True)
	password = db.Column(db.String(128))

    def hash_password(self, password):
        pass

    def verify_password(self, password):
        pass
