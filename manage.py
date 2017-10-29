import os
from application import create_app, db
from flask.ext.script import Manager, Shell

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)
