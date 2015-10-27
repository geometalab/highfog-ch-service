'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Models for DB OR mapping
'''
from data import db
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from geojson import Feature, FeatureCollection


class Height(db.Model):
    __tablename__ = 'heights'

    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=False))



class Peak(db.Model):
    __tablename__ = 'peaks'

    osm_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    height = db.Column(db.Float)
    geometry = db.Column(Geometry('POINT'))

    @staticmethod
    def to_geojson(query, max_forecasted_fog_height):
        peaks = []
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


class PublicTransport(db.Model):
    __tablename__ = 'public_transport'

    osm_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    geometry = db.Column(Geometry('POINT'))
    uic_name = db.Column(db.Text)
    height = db.Column(db.Float)
    gtype = db.Column(db.Text)

    @staticmethod
    def to_geojson(query_result, max_forecasted_fog_height):
        stops = []
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
