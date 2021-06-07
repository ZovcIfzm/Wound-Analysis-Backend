
import pathlib

SECRET_KEY = 'the quick brown fox jumps over the lazy   dog'
CORS_HEADERS = 'Content-Type'
PROJ_ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL_PATH = PROJ_ROOT/'wound_analysis'/'api'/'siamese_model'