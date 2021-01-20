
# [START gae_python38_app]

# This commmand, $env:FLASK_APP = "__init__.py", is needed in order for the api to be run.

import flask

app = flask.Flask(__name__, static_folder='../frontend/build',
                    static_url_path='/')

app.config.from_object('wound_analysis.config')
app.config.from_envvar('PROJ_SETTINGS', silent=True)

import wound_analysis.api

print('__init__.py ran manually')
# [END gae_python38_app]



@wound_analysis.app.route('/testMain2/', methods=['POST', 'GET'])
def testMain2():
    print('__init__.py ran')
    return "__init__.py ran in api"
