'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Models for DB OR mapping
'''
from data import db
from geoalchemy2 import Geometry

db = db


class Heights(db.Model):
    __tablename__ = 'heights'

    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=False))


class Pois(db.Model):
    __tablename__ = 'pois'

    osm_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    height = db.Column(db.Float)
    geometry = db.Column(Geometry('POINT'))


class PublicTransport(db.Model):
    __tablename__ = 'public_transport'

    osm_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    geometry = db.Column(Geometry('POINT'))
    uic_name = db.Column(db.Text)
    height = db.Column(db.Float)