'''
Created: 08.04.2015
@author: Dennis Ligtenberg
'''
import psycopg2
from ext_config import EOSM_LOGIN
from models import PublicTransport, db
from webservice import app


# Register an app for SQLAlchemy so this script can be executed standalone
db.init_app(app)
db.app = app

conn = psycopg2.connect(EOSM_LOGIN)
cursor = conn.cursor()
cursor.execute("""
    SELECT DISTINCT ON (osm_id) osm_id, name, ST_AsText (way), tags -> 'uic_name' as uic_name
    FROM osm_poi
    WHERE
    tags @> hstore('highway', 'bus_stop')
    OR tags @> hstore('public_transport', 'station')
    OR tags @> hstore('amenity', 'bus_station')
    OR hstore(tags)->'railway' IN ('stop', 'station', 'funicular', 'halt')
    order by osm_id asc;
""")
if cursor.rowcount:
    db.session.query(PublicTransport).delete()
    for row in cursor:
        new_entry = PublicTransport(
            osm_id=row[0],
            name=row[1],
            geometry=row[2],
            uic_name=row[3],
        )
        db.session.add(new_entry)
        db.session.commit()
    cursor.close()
    print '--------------------------------'
    print 'Done!'

else:
    cursor.close()
    print '--------------------------------'
    print 'No results!'