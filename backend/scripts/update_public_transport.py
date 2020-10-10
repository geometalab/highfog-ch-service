"""
Created: 08.04.2015
@author: Dennis Ligtenberg
Script for updating public transport stops from EOSMDBOne
"""
import psycopg2
import csv
from pathlib import Path

from config.ext_config import EOSM_LOGIN
from webservice.models import PublicTransport, db
from webservice import app


# Register an app for SQLAlchemy so this script can be executed standalone
db.init_app(app)
db.app = app


def load_existing_data():
    '"osm_id","name","st_astext","uic_name","gtype"'
    peaks_file_path = Path(__file__).parent / "initial_data" / "public_transport.csv"
    with open(peaks_file_path, newline="") as csvfile:
        public_transports = csv.reader(csvfile)
        db.session.query(PublicTransport).delete()
        for row in public_transports:
            new_entry = PublicTransport(
                osm_id=row[0],
                name=row[1],
                geometry=row[2],
                uic_name=row[3],
                gtype=row[4],
            )
            db.session.add(new_entry)
            db.session.commit()


def update_from_db():
    conn = psycopg2.connect(EOSM_LOGIN)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DISTINCT ON (osm_id) osm_id, name, ST_AsText (way), tags -> 'uic_name' as uic_name, gtype
        FROM osm_poi
        WHERE
        tags @> hstore('highway', 'bus_stop')
        OR tags @> hstore('public_transport', 'station')
        OR tags @> hstore('amenity', 'bus_station')
        OR hstore(tags)->'railway' IN ('stop', 'station', 'funicular', 'halt')
        order by osm_id asc;
    """
    )
    if cursor.rowcount:
        db.session.query(PublicTransport).delete()
        for row in cursor:
            new_entry = PublicTransport(
                osm_id=row[0],
                name=row[1],
                geometry=row[2],
                uic_name=row[3],
                gtype=row[4],
            )
            db.session.add(new_entry)
            db.session.commit()
        cursor.close()
        print("--------------------------------")
        print("Done!")

    else:
        cursor.close()
        print("--------------------------------")
        print("No results!")


def run_update():
    try:
        update_from_db()
    except Exception as e:
        print(e)
        print("couldn't connect to OSMDBOne")
        load_existing_data()
        print("loaded preexisting data from October 2020")
    finally:
        print(
            f"Done Updating Public Transport, containing {db.session.query(PublicTransport).count()}"
        )


if __name__ == "__main__":
    run_update()
