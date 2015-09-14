'''
Created: 08.04.2015
@author: Dennis Ligtenberg
'''
from models import db, Heights, Pois, PublicTransport
from shapely.geometry import geo
from geoalchemy2 import func
from geoalchemy2.shape import to_shape
from shapely.wkt import dumps
from geojson import Feature, FeatureCollection
from datetime import timedelta
from ext_config import FORECAST_INTERVAL


def get_heights():
    # Returns a dict with the fogheight forecast
    heights = []
    query_result = db.session.query(Heights).all()
    for row in query_result:
        heights.append({'height': row.height, 'date': row.date.strftime("%y-%m-%d %H:%M:%S")})
    return heights


def get_max_forecasted_height_by_time(time):
    # Get a height forecast at a certain time
    if time.hour % FORECAST_INTERVAL != 0:
        time += timedelta(hours=1)
    query = db.session.query(Heights).filter(Heights.date == time).first()
    if query:
        return query.height
    else:
        return 0


def get_peaks_at_forecasted_date(timestamp):
    # Returns a FeatureCollection with all peaks forecasted to be above the fog hours from now.
    peaks = []
    if timestamp.hour % FORECAST_INTERVAL != 0:
        timestamp += timedelta(hours=1)

    max_forecasted_fog_height = get_max_forecasted_height_by_time(timestamp)

    query = db.session.query(Pois).all()
    for row in query:
        geometry = to_shape(row.geometry)
        if row.height >= max_forecasted_fog_height:
            forecasted_above_fog = True
        else:
            forecasted_above_fog = False
        feature = Feature(
            id=row.osm_id,
            geometry=geometry,
            properties={
                "above_fog": forecasted_above_fog,
                "name": row.name,
                "height": row.height
            }
        )
        peaks.append(feature)
    return FeatureCollection(peaks)


def get_stops_within_bounds_at_forecasted_date(bounds, timestamp):
    # Returns a FeatureCollection with all public transport stops forecasted to be above the fog hours from now.
    stops = []

    max_forecasted_fog_height = get_max_forecasted_height_by_time(timestamp)

    bbox = geo.box(bounds['minx'], bounds['miny'], bounds['maxx'], bounds['maxy'])
    query_result = db.session.query(PublicTransport).filter(func.ST_Within(PublicTransport.geometry, dumps(bbox))).all()

    for row in query_result:
        if row.height >= max_forecasted_fog_height:
            forecasted_above_fog = True
        else:
            forecasted_above_fog = False
        geometry = to_shape(row.geometry)
        feature = Feature(
            id=row.osm_id,
            geometry=geometry,
            properties={
                "name": row.name,
                "above_fog": forecasted_above_fog,
                "height": row.height,
                "uic_name": row.uic_name,
                "gtype": row.gtype
            }
        )
        stops.append(feature)
    return FeatureCollection(stops)
