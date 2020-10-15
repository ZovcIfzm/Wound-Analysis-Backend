
# [START gae_python38_app]
import flask


app = flask.Flask(__name__, static_folder='../frontend/build/static',
                  static_url_path='/')

app.config.from_object('wound_analysis.config')
app.config.from_envvar('PROJ_SETTINGS', silent=True)

import wound_analysis.api

print('test2')
# [END gae_python38_app]



@wound_analysis.app.route('/testMain2/', methods=['POST', 'GET'])
def testMain2():
    return "hi2"
