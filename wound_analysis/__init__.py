
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('wound_analysis.config')

#app.config.from_object('wound_analysis.config')
#app.config.from_envvar('PROJ_SETTINGS', silent=True)
import wound_analysis.api
