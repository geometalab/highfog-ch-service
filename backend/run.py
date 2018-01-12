'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Runs the Flask app locally
'''
import os
from webservice import app

if __name__ == '__main__':
    from raven.contrib.flask import Sentry
    sentry = Sentry()  # automatically reads 'SENTRY_DSN' if set
    sentry.init_app(app)
    app.run(port=8080, debug=bool(os.environ.get('DEBUG')))
