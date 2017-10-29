from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from flask_sqlalchemy import SQLAlchemy 
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yuhack.db'
db = SQLAlchemy(app)

## SQL Configuration
app.config['MYSQL_USER'] = 'avi'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'YUhackathon'
app.config['MYSQL_HOST'] = '162.243.186.103'
app.config['MYSQL_PORT'] = '33067'
mysql = MySQL()
mysql.init_app(app)

db = mysql.connection
cursor = db.cursor()

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, nullable = False, primary_key = True, unique = True)
	name = db.Column('name', db.String(), nullable = False)
	email = db.Column('email', db.String(), nullable = False, unique = True)
	username = db.Column('username', db.String(), nullable = False, unique = True)
	password = db.Column('password', db.String(), nullable = False)

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
		newUser = User(name = form.name.data, email = form.email.data, username = 
			form.username.data, password = sha256_crypt.encrypt(str(form.password.data)))
		db.session.add(newUser)
		db.session.commit()
		#cursor.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data))) )		
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
	if(request.method == 'POST'):
		uname = request.form['username']
		pword = request.form['password']
		#result = cursor.execute("SELECT * FROM users WHERE username = %s", form.username.data)
		result = User.query.filter_by(username = uname).first()
		if result:
			if uname == result.username and sha256_crypt.verify(pword, result.password):
				session['logged_in'] = True
				session['username'] = uname
				return redirect(url_for('index'))
			else:
				return render_template('login.html')
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/gdash')
def gdash():
	return render_template('gdash.html')

@app.route('/pdash')
def pash():
	return render_template('pdash.html')

if __name__ == '__main__':
	app.run(debug = True)