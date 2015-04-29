'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Runs the Flask app locally
'''
from webservice import app
app = app
if __name__ == '__main__':
    app.run(port=55555)