from raven.contrib.flask import Sentry
from run import app as application

sentry = Sentry()  # automatically reads 'SENTRY_DSN' if set
sentry.init_app(application)
