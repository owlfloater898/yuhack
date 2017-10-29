from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
		#cursor.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data))) )		
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
	form = Login(request.form)
	if(request.method == 'POST' and form.validate()):
		#result = cursor.execute("SELECT * FROM users WHERE username = %s", form.username.data)
		if result:
			if result[3] == form.username.data and sha256_crypt.verify(form.password.data, result[4]):
				session['logged_in'] = True
				session['username'] = result[3]
				session['id'] = result[0]
				return redirect(url_for('index'))
			else:
				return render_template('login.html', form = form)
		else:
			return render_template('login.html', form = form)
	else:
		return render_template('login.html', form = form)

@app.route('/gdash')
def gdash():
	return render_template('gdash.html')

@app.route('/pdash')
def pash():
	return render_template('pdash.html')

if __name__ == '__main__':
	app.run(debug = True)