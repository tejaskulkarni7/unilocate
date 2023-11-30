import email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, FileField, SelectField
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
    #function to check if school id already exists
    def validate_school_id(self, school_id_to_check):
        school_id = User.query.filter_by(school_id = school_id_to_check.data).first()
        if school_id:
            raise ValidationError('School ID already exists!')


    #Form fields with validators to check for empty input, really short or long length, no empty field in the form
    username = StringField(label='Username', validators=[InputRequired(message="Username required"), Length(min=4, max=32, message="Username must be between 4 and 32 characters"), DataRequired()])
    email_address=StringField(label='Email', validators=[Email(message="Invalid Email address"), DataRequired()])
    password1 = PasswordField(label='Password', validators=[InputRequired(message="Password required"), Length(min=4, max=32, message="Password must be between 4 and 32 characters"), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[InputRequired(message="Password required"), EqualTo('password1', message="Passwords must match"), DataRequired()])
    school_id = StringField(label='School ID', validators=[InputRequired(message="ID required"), DataRequired()])
    submit = SubmitField(label='Submit')






#Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username required"), DataRequired()])
    password = PasswordField('Password', validators=[InputRequired(message="Password required"), DataRequired()])
    submit = SubmitField('Log In')


#Searching form
class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    filter_by = SelectField('Filter By', choices=[('all', 'All'), ('lost', 'Lost'), ('found', 'Found')], default='all')
    submit = SubmitField('Submit')                  #Submit button for searching


#Password form fields with validators to check for empty input, really short or long length, no empty field in the form
#Change Password form
class PasswordForm(FlaskForm):
    currentpass = PasswordField(label='Enter Current Password', validators=[InputRequired(message="Password required"), DataRequired()])
    newpass = PasswordField(label='Enter New Password', validators=[InputRequired(message="Password required"), Length(min=4, max=32, message="Password must be between 4 and 32 characters"), DataRequired()])
    submit = SubmitField(label='Submit')


class LostItemForm(FlaskForm):
    item_name = StringField(label='Name of Lost Item', validators=[InputRequired(message="Item name required"), DataRequired()])
    item_type = StringField(label='Type of Lost Item', validators=[InputRequired(message="Item type required"), DataRequired()])
    lost_location = StringField(label='Location of Lost Item (Optional)')
    description = StringField(label='Description of Lost Item', validators=[InputRequired(message="Item description required"), DataRequired()])
    image = FileField(label='Upload Image', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField(label='Submit')


class FoundItemForm(FlaskForm):
    item_name = PasswordField(label='Name of Found Item', validators=[InputRequired(message="Item required"), DataRequired()])
    item_type = StringField(label='Type of Lost Item', validators=[InputRequired(message="Item type required"), DataRequired()])
    found_location = StringField(label='Found Location', validators=[InputRequired(message="Found location required"), DataRequired()])
    current_location = StringField(label='Current Location', validators=[InputRequired(message="Current location required"), DataRequired()])
    description = StringField(label='Name of Lost Item', validators=[InputRequired(message="Item description required"), DataRequired()])
    image = FileField(label='Upload Image', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField(label='Submit')