import email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, FileField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, DataRequired, Email
from app.models import User

#Sign Up form
class RegistrationForm(FlaskForm):
	
	#function to check if username already exists
	def validate_username(self, username_to_check):
		user = User.query.filter_by(username = username_to_check.data).first()
		if user:
			raise ValidationError('Username already exists! Please try different username.')

	#function to check if email already exists
	def validate_email_address(self, email_address_to_check):
		email_address = User.query.filter_by(email_address = email_address_to_check.data).first()
		if email_address:
			raise ValidationError('Email address already exists! Please try different email.')

	#Form fields with validators to check for empty input, really short or long length, no empty field in the form
	username = StringField(label='Username', validators=[InputRequired(message="Username required"), Length(min=4, max=32, message="Username must be between 4 and 32 characters"), DataRequired()])
	email_address=StringField(label='Email', validators=[Email(message="Invalid Email address"), DataRequired()])
	password1 = PasswordField(label='Password', validators=[InputRequired(message="Password required"), Length(min=4, max=32, message="Password must be between 4 and 32 characters"), DataRequired()])
	password2 = PasswordField(label='Confirm Password', validators=[InputRequired(message="Password required"), EqualTo('password1', message="Passwords must match"), DataRequired()])
	school_id = StringField(label='School ID', validators=[InputRequired(message="School ID required"), Length(min=9, max=9, message="ID must have 9 numbers"), DataRequired()])
	phone_number = StringField(label='Phone Number', validators=[InputRequired(message="Phone number required"), Length(min=10, max=15, message="Phone number must be between 10 and 15 numbers"), DataRequired()])
	submit = SubmitField(label='Submit')



#Login form
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(message="Username required"), DataRequired()])
	password = PasswordField('Password', validators=[InputRequired(message="Password required"), DataRequired()])
	submit = SubmitField('Log In')

#Searching form
class SearchForm(FlaskForm):
	searched = StringField('Searched', validators=[DataRequired()])
	submit = SubmitField('Submit')					#Submit button for searching

#Password form fields with validators to check for empty input, really short or long length, no empty field in the form
#Change Password form
class PasswordForm(FlaskForm):
	currentpass = PasswordField(label='Enter Current Password', validators=[InputRequired(message="Password required"), DataRequired()]) 
	newpass = PasswordField(label='Enter New Password', validators=[InputRequired(message="Password required"), Length(min=4, max=32, message="Password must be between 4 and 32 characters"), DataRequired()])
	submit = SubmitField(label='Submit')

class LostItemForm(FlaskForm):
	item = PasswordField(label='Name of Lost Item', validators=[InputRequired(message="Item required"), DataRequired()])
	submit = SubmitField(label='Submit')

class FoundItemForm(FlaskForm):
	item = PasswordField(label='Name of Found Item', validators=[InputRequired(message="Item required"), DataRequired()])
	submit = SubmitField(label='Submit')