'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Create and setup Flask app, register blueprints with views.
'''
from flask import Flask
from views import web_service

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
app.register_blueprint(web_service)
from data import db

db.init_app(app)