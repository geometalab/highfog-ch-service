'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify
from update_fog_height import UpdateFogHeight
from models import Heights, Pois, db
from geojson import Feature, FeatureCollection, dumps
from geoalchemy2.shape import to_shape
from json import loads

webservice = Blueprint("webservice", __name__)


@webservice.route('/v1/')
def index():
    return 'Welcome to the highfog webservice!'


@webservice.route('/v1/fogmap')
def fogmap():
    return jsonify({'Fog': 'Here', 'NoFog': 'There'})


@webservice.route('/v1/update')
def update():
    UpdateFogHeight().update()
    return 'Data Updated'


@webservice.route('/v1/heights')
def get_heights():
    heights = []
    query = db.session.query(Heights).all()
    for row in query:
        heights.append({'height': row.height, 'date': row.date.strftime("%y-%m-%d %H:%M:%S")})
    return jsonify(heights=heights)


@webservice.route('/v1/pois/')
def get_pois():
    pois = []
    query = db.session.query(Pois).all()

    for row in query:
        geometry = to_shape(row.geometry)
        feature = Feature(
            id=row.osm_id,
            geometry=geometry,
            properties={
                "name": row.name,
                "height": row.height
            }
        )
        pois.append(feature)
    return jsonify(loads(dumps(FeatureCollection(pois))))