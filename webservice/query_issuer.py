'''
Created: 08.04.2015
@author: Dennis Ligtenberg
'''
from datetime import timedelta

from shapely.geometry import geo
from geoalchemy2 import func
from shapely.wkt import dumps
from .models import db, Height, Peak, PublicTransport
from config.ext_config import FORECAST_INTERVAL


def get_heights():
    # Returns a dict with the fogheight forecast
    heights = []
    query_result = db.session.query(Height).all()
    for row in query_result:
        heights.append({'height': row.height, 'date': row.date.strftime("%y-%m-%d %H:%M:%S")})
    return heights


def get_max_forecasted_height_by_time(time):
    # Get a height forecast at a certain time
    if time.hour % FORECAST_INTERVAL != 0:
        time += timedelta(hours=1)
    query = db.session.query(Height).filter(Height.date == time).first()
    if query:
        return query.height
    else:
        return 0


def get_peaks():
    # Returns a FeatureCollection with all peaks forecasted to be above the fog hours from now.
    results = db.session.query(Peak).all()
    return results

def get_stops_within_bounds(bounds):
    # Returns a FeatureCollection with all public transport stops
    bbox = geo.box(bounds['minx'], bounds['miny'], bounds['maxx'], bounds['maxy'])
    return db.session.query(PublicTransport).filter(func.ST_Within(PublicTransport.geometry, dumps(bbox))).all()
