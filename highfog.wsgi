activate_this = '/home/ifs/PythonApps/highfog-ch-service/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/ifs/PythonApps/highfog-ch-service')
reload(sys)
sys.setdefaultencoding('utf-8')
from run  import app as application