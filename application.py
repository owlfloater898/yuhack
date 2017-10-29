#helloworld
from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

class Register(Form):
	name = StringField('Name', [validators.DataRequired()])
	email = StringField('Email', [validators.Email(message='Invalid email address')])
	username = StringField('Username', [validators.Length(min = 5, max = 25)])
	password = PasswordField('Password', [validators.Length(min = 5, max = 25), validators.EqualTo('confirm', message='Passwords do not match')])
	confirm = PasswordField('Confirm Password')

class Login(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.Length(min = 5, max = 25)])

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
	form = Register(request.form)
	if(request.method == 'POST' and form.validate()):
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
	form = Login(request.form)
	if(request.method == 'POST' and form.validate()):
		return redirect(url_for('index'))
	else:
		return render_template('login.html', form = form)

@app.route('/gdash')
def gdash():
	return render_template('gdash.html')

@app.route('/pdash')
def pash():
	return render_template('pdash.html')

if __name__ == '__main__':
	app.secret_key = 'supersecretkey'
	app.run(debug = True)