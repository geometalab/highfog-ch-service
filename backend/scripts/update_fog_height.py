import os
import requests

r = requests.get(os.environ['INTERNAL_UPDATE_HOST'] + '/v1/update')
assert r.status_code == 200

print('Done!')
