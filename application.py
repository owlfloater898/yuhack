from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from flask_sqlalchemy import SQLAlchemy 
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yuhack.db'
db = SQLAlchemy(app)

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
	amount = StringField('Amount', [validators.DataRequired()])
	description = TextAreaField('Description' )
	tags = StringField('Tags', [validators.DataRequired()])
	location = StringField('Location', [validators.DataRequired()])

class PropsForm(Form):
	title = StringField('Title', [validators.Length(min = 5, max = 25)])
	amount = StringField('Amount', [validators.DataRequired()])
	description = TextAreaField('Description' )
	tags = StringField('Tags', [validators.DataRequired()])
	location = StringField('Location', [validators.DataRequired()])

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

@app.route('/gdash')
@login_required
def gdash():
	result = Grant.query.filter_by(userid = session['id']).all()
	return render_template('gdash.html', grants=result)

@app.route('/gdash_add', methods=['GET','POST'])
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

@app.route('/pdash')
@login_required
def pdash():
	results = Props.query.filter_by(userid = session['id']).all()
	return render_template('pdash.html', props=results)

@app.route('/pdash_add', methods=['GET','POST'])
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

@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True)