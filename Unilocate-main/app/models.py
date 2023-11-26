from app import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#User class in database with validators
class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(length=30), nullable=False, unique=True)
	email_address = db.Column(db.String(length=50), nullable=False, unique=True)
	password_hash = db.Column(db.String(length=60), nullable=False)
	school_id = db.Column(db.String(), nullable=False, unique=True)

	@property
	def password(self):
		return self.password

	@password.setter
	def password(self, plain_text_password):
		self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

	def check_password_correction(self, attempted_password):                       #function to check if pasword in the login form = password in db
		return bcrypt.check_password_hash(self.password_hash, attempted_password)


	def __repr__(self):
		return f'User {self.username}'


class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(length=100), nullable=False)
    item_type = db.Column(db.String(length=50), nullable=False)
    lost_location = db.Column(db.String(length=100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref='lost_items')
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    filename = db.Column(db.String(length=30), nullable=False)
    resolved = db.Column(db.Boolean, default=False)

class FoundItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	item_name = db.Column(db.String(length=100), nullable=False)
	item_type = db.Column(db.String(length=50), nullable=False)
	found_location = db.Column(db.String(length=100), nullable=False)
	current_location = db.Column(db.String(length=100), nullable=False)
	description = db.Column(db.Text, nullable=True)
	date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	user = db.relationship('User', backref='found_items')
	image = db.Column(db.String(20), nullable=False, default='default.jpg')
	filename = db.Column(db.String(length=30), nullable=False)
	resolved = db.Column(db.Boolean, default=False)
