'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Create and setup Flask app, register blueprints with views.
'''
from flask import Flask
from .views import webservice
from .data import db


app = Flask(__name__)
app.config.from_object('config.flask_config.BaseConfig')
app.register_blueprint(webservice)

db.init_app(app)
with app.app_context():
    db.create_all()
