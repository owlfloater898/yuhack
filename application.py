from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

class Register(Form):
	name = StringField('Name', [validators.DataRequired()])
	username = StringField('Username', [validators.Length(min = 5, max = 25)])
	password = PasswordField('password', [validators.Length(min = 5, max = 25)], validators.EqualTo('confirm', message='Passwords do not mathc'))
	confirm = PasswordField('Confirm Pasword')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
	form = Register(request.form)
	if(request.method == 'POST')
	return render_template('register')

@app.route('/login')
def login():
	return render_template('login')

@app.route('/gdash')
def gdash():
	return render_template('gdash.html')

@app.route('/pdash')
def pash():
	return render_template('pdash.html')

if __name__ == '__main__':
	app.secret_key = 'supersecretkey'
	app.run(debug = True)