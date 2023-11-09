from app.forms import RegistrationForm, LoginForm, SearchForm, PasswordForm, LostItemForm, FoundItemForm
from flask import render_template, redirect, url_for, request, flash
from app import myapp_obj, db
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
import os
@myapp_obj.route("/", methods=['GET', 'POST'])
def home():
	return render_template('home.html', title='Home')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def loginPage():
	form = LoginForm()
	if form.validate_on_submit():	#check if submit is clicked
		attempted_user = User.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data): #if the username and password are correct
			login_user(attempted_user) #then login the user session
			flash(f'Success logging in, Logged in as: {attempted_user.username}', category='success')
			return redirect(url_for('home'))
		else:
			flash('Username or Password does not match! Please try again', category='danger')
	return render_template('login.html', title='Login', form=form) 		

@myapp_obj.route('/logout')
def logoutPage():
	logout_user()
	flash("You have been logged out!", category='info')
	return redirect(url_for("home"))



	


  
@myapp_obj.route("/signup", methods=['GET', 'POST'])
def signupPage():
	form = RegistrationForm()  #signup form from forms.py
	if form.validate_on_submit():
		user_to_create = User(username=form.username.data, email_address=form.email_address.data, student_id = form.student_id.data, password=form.password1.data)	#get data from the form user filled
		db.session.add(user_to_create)
		db.session.commit()	#add it to database
		login_user(user_to_create)	#login the user if signup is successfull
		flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')	#flash success message
		return redirect(url_for('home'))	#redirect to market after logging in
	if form.errors != {}: #If there are errors in signing up
		for err_msg in form.errors.values():
				flash(f'There was an error with creating a user: {err_msg}', category='danger') #flash appropriate error message

	return render_template('signup.html', form=form, title='Signup')



@myapp_obj.route("/profilepage", methods=['GET', 'POST'])
def profile():
	if request.method == 'POST':
		if request.form.get('deleteprofile') == 'Delete Profile': #if the delete profile button is clicked
			userid2 = request.form.get('userid2')
			u = User.query.filter_by(id = userid2).first() #filter the User class for wherever the given userid is found
			db.session.delete(u) #delete the previously found user
			db.session.commit()
			flash('Profile Deleted!', category='success')
			return redirect(url_for('logoutPage')) #flash and redirect
		if request.form.get('changepassword') == 'Change Password':
			return redirect(url_for('changepassword'))
		else:
			None# unknown
	elif request.method == 'GET':
		return render_template('profilepage.html', title='My Profile')



@myapp_obj.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

@myapp_obj.route('/search', methods=["POST"])
@login_required
def search():
	form = SearchForm()




@myapp_obj.route('/changepassword', methods=["GET", "POST"])
def changepassword():
	form = PasswordForm()
	if form.validate_on_submit():	#check if submit is clicked
		currentpass = form.currentpass.data #get data for both the newpass and the current pass
		newpass = form.newpass.data 
		userid2 = request.form.get('userid2')
		u = User.query.filter_by(id = userid2).first() #find the user object in db
		if u.check_password_correction(currentpass): #check if the users password is the same as the entered "currentpass"
			u.password = form.newpass.data #override the current password in the db with the new one
			db.session.add(u)
			db.session.commit()
			flash("Your Password Has Been Changed", category='success')
			return render_template("changepassword.html", form=form)
		else: 
			flash("Incorrect Password", category='danger')
			return render_template("changepassword.html", form=form)
	return render_template("changepassword.html", form=form)


#---------------------------------------------


@myapp_obj.route('/lostitem', methods=["GET", "POST"])
@login_required
def lostitem():
	form = LostItemForm()
	if form.validate_on_submit():	#check if submit is clicked
		return render_template("home.html", form=form)
	return render_template("lostitem.html", form=form)


@myapp_obj.route('/founditem', methods=["GET", "POST"])
@login_required
def founditem():
	form = FoundItemForm()
	if form.validate_on_submit():	#check if submit is clicked
		return render_template("home.html", form=form)
	return render_template("founditem.html", form=form)

@myapp_obj.route('/infopage', methods=["GET"])
@login_required
def infopage():
	return render_template("infopage.html")