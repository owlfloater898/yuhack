from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, TextAreaField, DecimalField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from collections import Counter


application = Flask(__name__)
application.secret_key = 'supersecretkey'

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:85878500@yudbinstance.ct86rbi71o0x.us-west-2.rds.amazonaws.com:3306/YUhackathon'
db = SQLAlchemy(application)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, nullable = False, primary_key = True, unique = True)
	name = db.Column('name', db.String(), nullable = False)
	email = db.Column('email', db.String(), nullable = False, unique = True)
	username = db.Column('username', db.String(), nullable = False, unique = True)
	password = db.Column('password', db.String(), nullable = False)

class Grant(db.Model):
	__tablename__ = 'grants'
	id = db.Column('id', db.Integer, nullable = False, primary_key = True, unique = True)
	userid = db.Column('userid', db.Integer, nullable = False)
	amount = db.Column('amount', db.Integer, nullable = False, )
	description = db.Column('description', db.String(), nullable = False, )
	tags = db.Column('tags', db.String(), nullable = False)
	location = db.Column('location', db.String(), nullable = False)

class Props(db.Model):
	__tablename__ = 'proposals'
	id = db.Column('id', db.Integer, nullable = False, primary_key = True, unique = True)
	userid = db.Column('userid', db.Integer, nullable = False)
	title = db.Column('title', db.String(), nullable = False)
	amount = db.Column('amount', db.Integer, nullable = False)
	description = db.Column('description', db.String(), nullable = False, )
	tags = db.Column('tags', db.String(), nullable = False)
	location = db.Column('location', db.String(), nullable = False)

class Register(Form):
	name = StringField('Name', [validators.DataRequired()])
	email = StringField('Email', [validators.Email(message='Invalid email address')])
	username = StringField('Username', [validators.Length(min = 5, max = 25)])
	password = PasswordField('Password', [validators.Length(min = 5, max = 25), validators.EqualTo('confirm', message='Passwords do not match')])
	confirm = PasswordField('Confirm Password')

class Login(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.Length(min = 5, max = 25)])

class GrantForm(Form):
	amount = DecimalField('Amount', [validators.NumberRange(min = 100, max = None)])
	description = TextAreaField('Description' )
	tags = StringField('Tags', [validators.DataRequired()])
	location = StringField('Location', [validators.DataRequired()])

class PropsForm(Form):
	title = StringField('Title', [validators.Length(min = 5, max = 25)])
	amount = DecimalField('Amount', [validators.NumberRange(min = 100, max = None)])
	description = TextAreaField('Description' )
	tags = StringField('Tags', [validators.DataRequired()])
	location = StringField('Location', [validators.DataRequired()])

class Search(Form):
	tags = StringField('Tags', [validators.DataRequired()])

@application.route('/', methods =['GET', 'POST'])
def index():
	#form = Search(request.form)
	#if request.method == 'POST' and form.validate()):
	#	return redirect(url_for('login'))
	#else:
		return render_template('index.html')

@application.route('/about')
def about():
	return render_template('about.html')

@application.route('/results')
def results():
	tags = request.form.get('tags')
	props = Props.query.filter_by(tags = tags).all()
	grants = Grant.query.filter_by(tags = tags).all()
	return render_template('index.html', grants = grants, props = props)

@application.route('/register', methods=['GET','POST'])
def register():
	form = Register(request.form)
	if(request.method == 'POST' and form.validate()):
		newUser = User(name = form.name.data, email = form.email.data, username =
			form.username.data, password = sha256_crypt.encrypt(str(form.password.data)))
		db.session.add(newUser)
		db.session.commit()
		#cursor.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data))) )
		return redirect(url_for('login'))
	else:
		return render_template('register.html', form = form)

@application.route('/login', methods=['GET','POST'])
def login():
	if(request.method == 'POST'):
		username = request.form['username']
		password = request.form['password']
		#result = cursor.execute("SELECT * FROM users WHERE username = %s", form.username.data)
		result = User.query.filter_by(username = username).first()
		if result:
			if username == result.username and sha256_crypt.verify(password, result.password):
				session['logged_in'] = True
				session['username'] = username
				session['id'] = result.id
				return redirect(url_for('index'))
			else:
				return render_template('login.html')
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')

#ensure that the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@application.route('/gdash')
@login_required
def gdash():
	myGrants = Grant.query.filter_by(userid = session['id']).all()
	props = Props.query.filter(Props.userid != session['id']).all()
	matches = []
	for myGrant in myGrants:
		for prop in props:
			common = set(myGrant.tags.split()) & set(prop.tags.split())
			if common:
				matches.append(prop)
	uniqueMatches = []
	#remove duplicates by making a new list and only adding things to it if they aren't already in it
	#that way, when a duplicate comes up, it won't be added because it's already there
	for match in matches:
		if match not in uniqueMatches:
			uniqueMatches.append(match)
	return render_template('gdash.html', grants=myGrants, props=uniqueMatches)

@application.route('/gdash_add', methods=['GET','POST'])
@login_required
def gdash_add():
	form = GrantForm(request.form)
	if request.method == 'POST' and form.validate():
		newGrant = Grant(userid = session['id'], amount = form.amount.data, description = form.description.data, tags =
			form.tags.data, location = form.location.data)
		db.session.add(newGrant)
		db.session.commit()
		return redirect(url_for('gdash'))
	else:
		return render_template('gdash_add.html', form=form)

@application.route('/pdash')
@login_required
def pdash():
	myProps = Props.query.filter_by(userid = session['id']).all()
	grants = Grant.query.filter(Grant.userid != session['id']).all()
	matches = []
	for myprop in myProps:
		for grant in grants:
			common = set(myprop.tags.split()) & set(grant.tags.split())
			if common:
				matches.append(grant)
	uniqueMatches = []
	#remove duplicates by making a new list and only adding things to it if they aren't already in it
	#that way, when a duplicate comes up, it won't be added because it's already there
	for match in matches:
		if match not in uniqueMatches:
			uniqueMatches.append(match)
	return render_template('pdash.html', props=myProps, grants=uniqueMatches)

@application.route('/pdash_add', methods=['GET','POST'])
@login_required
def pdash_add():
	form = PropsForm(request.form)
	if request.method == 'POST' and form.validate():
		newProp = Props(userid = session['id'], title = form.title.data, amount = form.amount.data, description = form.description.data, tags =
			form.tags.data, location = form.location.data)
		db.session.add(newProp)
		db.session.commit()
		return redirect(url_for('pdash'))
	else:
		return render_template('pdash_add.html', form=form)

@application.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))

if __name__ == '__main__':
	application.run(debug = True)
