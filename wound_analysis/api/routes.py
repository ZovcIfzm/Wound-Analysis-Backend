
# [START gae_python38_app]
import flask
import os
from werkzeug.utils import secure_filename
import cv2
import time

import pathlib
import uuid

import wound_analysis

from wound_analysis.api.area_optimization import default_measurement, optimized_masking_measurement, manual_area_adjustment
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.

global test_val
test_val = 0
global data
data = {}


wound_analysis.app.secret_key = \
    b't\xc7\xe7\xbd(P1+\xb77]\xc1\xf4H\\\xd0\x8b.\r+|g\x8a\x83'

@wound_analysis.app.route('/time/')
def get_current_time():
    return {'time': time.time()}


@wound_analysis.app.route('/post/', methods=['POST', 'GET'])
def post():
    print("reached post")
    fileobj = flask.request.files["file"]

    fileobj.save(os.path.join(wound_analysis.app.root_path, "cur_image.jpg"))
    print("post saved")
    return flask.redirect("/")


@wound_analysis.app.route('/testPrint/', methods=['POST', 'GET'])
def show_time():
    print("tested")
    return {"test": "testedInFlask"}


@wound_analysis.app.route('/analyze/', methods=['POST', 'GET'])
def run_recog():
    global data
    global test_val
    filename = flask.request.form.get("filename")
    mode = flask.request.form.get("mode")
    img_url = str(wound_analysis.app.config["UPLOAD_FOLDER"]/filename)
    const_img_url = str(wound_analysis.app.config["UPLOAD_FOLDER"]/"analyzed.png")
    if mode == "run":
        width = float(flask.request.form.get("width"))
        print(width)
        image = cv2.imread(img_url)
        data = optimized_masking_measurement(image, width)
        cv2.imwrite(img_url, data["drawn_image"])
        cv2.imwrite(const_img_url, data["drawn_image"])
        print("img url ok: ", img_url)
        print("img url ok: ", const_img_url)
        return {"analyzed": True}

    elif mode == "increase sat":
        width = float(flask.request.form.get("width"))
        data = manual_area_adjustment(data, True)
        print("printing data")
        # print(data)

        cv2.imwrite('cur_image.jpg', data["drawn_image"])
    elif mode == "decrease sat":
        width = float(flask.request.form.get("width"))
        data = manual_area_adjustment(data, False)
        print("printing data")
        # print(data)
        cv2.imwrite('cur_image.jpg', data["drawn_image"])
    elif mode == "test":
        test_val += 2
        print(test_val)

    return flask.redirect("/")


@wound_analysis.app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return wound_analysis.app.send_static_file("index.html")

@wound_analysis.app.route('/upload/',  methods=['POST', 'GET'])
def upload():
    # Connect to database
    connection = wound_analysis.model.get_db()

    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    # Compute base name (filename without directory).  We use a UUID
    # to avoid clashes with existing files, and ensure that the name
    # is compatible with the filesystem.
    uuid_basename = filename
    '''
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )'''

    # Save to disk
    path = wound_analysis.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    
    '''
    connection.execute(
        "INSERT INTO images(filename)"
        "VALUES(?)", (uuid_basename,)
    )'''
    return {"filename": filename}
    
@wound_analysis.app.route('/database/', methods=['POST', 'GET'])
def testDataBase():
    return "tested"

@wound_analysis.app.route('/database/uploads/<path:filename>', methods=['POST', 'GET'])
def download_file(filename):
    return flask.send_from_directory(wound_analysis.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)

def parse_url(url):
    split_url = url.split('\\')
    return "\\\\".join(split_url)

def parse_display(url):
    split_url = url.split('\\\\')
    return "".join(split_url)

# [END gae_python38_app]
