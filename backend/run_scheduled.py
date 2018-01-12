from __future__ import print_function
import datetime
import logging
import os
import schedule
import subprocess
import time

from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

logger = logging.getLogger(__name__)
sentry_dsn = os.environ.get('SENTRY_DSN')

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

if sentry_dsn:
    client = Client(sentry_dsn)
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    setup_logging(handler)
else:
    logging.basicConfig()


def log_execution(command, *args, **kwargs):
    try:
        result = command(*args, **kwargs)
    except:
        logger.error("execption occurred while using {} with {} and {}".format(command, args, kwargs), exc_info=True)
        raise
    if result:
        print(result)


def update_heights():
    log_execution(subprocess.check_output, ['python', os.path.join(BASE_PATH, 'scripts/update_heights.py')], env=os.environ)


def update_peaks():
    log_execution(subprocess.check_output, ['python', os.path.join(BASE_PATH, 'scripts/update_peaks.py')], env=os.environ)


def update_public_transport():
    log_execution(subprocess.check_output, ['python', os.path.join(BASE_PATH, 'scripts/update_public_transport.py')], env=os.environ)


def update_fog_height():
    log_execution(subprocess.check_output, ['python', os.path.join(BASE_PATH, 'scripts/update_fog_height.py')], env=os.environ)


if __name__ == '__main__':
    print("updater started")
    # run once, scheduled for later run after this
    print("updating fog height")
    update_fog_height()
    print("updating heights")
    update_heights()
    print("updating peaks")
    update_peaks()
    print("updating public transport")
    update_public_transport()

    # only the fog height needs to be scheduled
    schedule.every(30).minutes.do(update_fog_height)

    while True:
        schedule.run_pending()
        time.sleep(60)  # 1 Minute
