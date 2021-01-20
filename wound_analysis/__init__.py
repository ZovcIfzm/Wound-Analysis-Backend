
from flask import Flask

app = Flask(__name__)

#app.config.from_object('wound_analysis.config')
#app.config.from_envvar('PROJ_SETTINGS', silent=True)
'''
print('__init__.py ran manually')

@wound_analysis.app.route('/testMain2/', methods=['POST', 'GET'])
def testMain2():
    print('__init__.py ran')
    return "__init__.py ran in api"
'''
#import wound_analysis.api
