'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify, request
from update_fog_height import UpdateFogHeight
from models import Heights, Pois, db
from geojson import Feature, FeatureCollection
from geoalchemy2.shape import to_shape
from geoalchemy2 import func
from shapely.geometry import geo
from shapely.wkt import dumps
from crossdomain import crossdomain


webservice = Blueprint("webservice", __name__)


@webservice.route('/v1/')
def index():
    return 'Welcome to the highfog webservice!'


@webservice.route('/v1/fogmap')
@crossdomain(origin='*')
def fogmap():
    return jsonify({'Fog': 'Here', 'NoFog': 'There'})


@webservice.route('/v1/update')
@crossdomain(origin='*')
def update():
    UpdateFogHeight().update()
    return 'Data Updated'


@webservice.route('/v1/heights')
@crossdomain(origin='*')
def get_heights():
    heights = []
    query = db.session.query(Heights).all()
    for row in query:
        heights.append({'height': row.height, 'date': row.date.strftime("%y-%m-%d %H:%M:%S")})
    return jsonify(heights=heights)


@webservice.route('/v1/pois/')
@crossdomain(origin='*')
def get_pois():
    # Dict with Bounds (minx, miny, maxx, maxy from the GET parameters)
    bounds = {
        'minx': float(request.args.get('minx')),
        'miny': float(request.args.get('miny')),
        'maxx': float(request.args.get('maxx')),
        'maxy': float(request.args.get('maxy'))
    }

    pois = []
    bbox = geo.box(bounds['minx'], bounds['miny'], bounds['maxx'], bounds['maxy'])
    query = db.session.query(Pois).filter(func.ST_Within(Pois.geometry, dumps(bbox))).all()

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
    return jsonify(FeatureCollection(pois))