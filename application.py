from flask import Flask, render_template, redirect, url_for, session, request, logging, jsonify, json, Response
from flask_api import status
from flask_sqlalchemy import SQLAlchemy 
from wtforms import Form, StringField, PasswordField, TextAreaField, DecimalField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from collections import Counter

application = Flask(__name__)
application.secret_key = 'supersecretkey'

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:85878500@yudbinstance.ct86rbi71o0x.us-west-2.rds.amazonaws.com:3306/YUhackathon'
db = SQLAlchemy(application)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, nullable = False, primary_key = True, unique = True)
	name = db.Column('name', db.String(), nullable = False)
	email = db.Column('email', db.String(), nullable = False, unique = True)
	username = db.Column('username', db.String(), nullable = False)
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

@application.route('/')
def index():
	if 'logged_in' in session:
		props = Props.query.filter(Props.userid != session['id']).all()
		grants = Grant.query.filter(Grant.userid != session['id']).all()
	else:
		props = Props.query.all()
		grants = Grant.query.all()
	return render_template('index.html', grants = grants, props = props)

@application.route('/register', methods=['POST'])
def register():
	content = request.json
	name = content["name"]
	email = content["email"]
	username = content["username"]
	password = content["password"]
	newUser = User(name = name, email = email, username = 
		username, password = sha256_crypt.encrypt(str(password)))
	if not newUser:
		return jsonify(error = 'CANNOT CREATE NEW USER'), status.HTTP_500_INTERNAL_SERVER_ERROR
	db.session.add(newUser)
	db.session.commit()
	return jsonify(id = newUser.id), status.HTTP_201_CREATED

@application.route('/login', methods=['GET','POST'])
def login():
	content = request.json
	username = content['username']
	password = content['password']
	result = User.query.filter_by(username = username).first()
	if result:
		if username == result.username and sha256_crypt.verify(password, result.password):
			session['logged_in'] = True
			session['username'] = username
			session['id'] = result.id
			return jsonify(id = result.id), status.HTTP_202_ACCEPTED
		else:
			return jsonify(error = 'INVALID USERNAME OR PASSWORD'), status.HTTP_500_INTERNAL_SERVER_ERROR
	else:
		return jsonify(error = 'COULD NOT FIND USER TABLE'), status.HTTP_500_INTERNAL_SERVER_ERROR

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
	if not myGrants or not props:
		return jsonify(error = 'COULD NOT FIND GRANTS OR PROPOSALS'), status.HTTP_500_INTERNAL_SERVER_ERROR
	matches = []
	for myGrant in myGrants:
		for prop in props:
			common = set(myGrant.tags.split()) & set(prop.tags.split())
			if common:
				matches.applicationend(prop)
	uniqueMatches = []
	#remove duplicates by making a new list and only adding things to it if they aren't already in it
	#that way, when a duplicate comes up, it won't be added because it's already there
	for match in matches:
		if match not in uniqueMatches:
			uniqueMatches.applicationend(match)
	return jsonify(grants = myGrants, matches = uniqueMatches), status.HTTP_200_OK

@application.route('/gdash_add', methods=['GET','POST'])
@login_required
def gdash_add():
	content = request.json
	amount = content['amount']
	description = content['description']
	tags = content['tags']
	location = content['location']
	newGrant = Grant(userid = session['id'], amount = amount, description = description, tags = 
	tags, location = location)
	db.session.add(newGrant)
	db.session.commit()
	return redirect(url_for('gdash'))
	
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
				matches.applicationend(grant)
	uniqueMatches = []
	#remove duplicates by making a new list and only adding things to it if they aren't already in it
	#that way, when a duplicate comes up, it won't be added because it's already there
	for match in matches:
		if match not in uniqueMatches:
			uniqueMatches.applicationend(match)
	return jsonify(props = myProps, matches = uniqueMatches), status.HTTP_200_OK

@application.route('/pdash_add', methods=['GET','POST'])
@login_required
def pdash_add():
	content = request.json
	title = content['title']
	amount = content['amount']
	description = content['description']
	tags = content['tags']
	location = content['location']
	newProp = Props(userid = session['id'], title = title, amount = amount, description = description, tags = 
	tags, location = location)
	db.session.add(newProp)
	db.session.commit()
	return redirect(url_for('pdash'))

@application.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))

if __name__ == '__main__':
	application.run(debug = True)
