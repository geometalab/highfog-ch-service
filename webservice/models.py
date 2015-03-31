'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Models for DB OR mapping
'''

from data import db

db = db


class Heights(db.Model):
    __tablename__ = 'heights'
    __bind_key__ = 'internal'

    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=False))
