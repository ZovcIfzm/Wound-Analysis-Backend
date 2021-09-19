
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config.from_object('wound_analysis.config')

import wound_analysis.api  # nopep8
# app.config.from_object('wound_analysis.config')
#app.config.from_envvar('PROJ_SETTINGS', silent=True)
