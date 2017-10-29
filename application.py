from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/gdash')
def gdash():
	return render_template('gdash.html')


@app.route('/pdash')
def pash():
	return render_template('pdash.html')

if __name__ == '__main__':
	app.secret_key = 'supersecretkey'
	app.run(debug = True)