
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


@wound_analysis.app.route('/recog/', methods=['POST', 'GET'])
def run_recog():
    if flask.request.method == 'POST':
        global data
        global test_val
        if flask.request.form.get("recog") is not None:
            value = flask.request.form.get("recog")
            img_url = "cur_image.jpg"
            if value == "run":
                width = float(flask.request.form.get("width"))
                print(width)
                image = cv2.imread(img_url)
                data = optimized_masking_measurement(image, width)
                print("printing data")

                cv2.imwrite('cur_image.jpg', data["drawn_image"])

            elif value == "increase sat":
                width = float(flask.request.form.get("width"))
                data = manual_area_adjustment(data, True)
                print("printing data")
                # print(data)

                cv2.imwrite('cur_image.jpg', data["drawn_image"])
            elif value == "decrease sat":
                width = float(flask.request.form.get("width"))
                data = manual_area_adjustment(data, False)
                print("printing data")
                # print(data)
                cv2.imwrite('cur_image.jpg', data["drawn_image"])
            elif value == "test":
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
    print("filename")

    # Compute base name (filename without directory).  We use a UUID
    # to avoid clashes with existing files, and ensure that the name
    # is compatible with the filesystem.
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )

    # Save to disk
    path = wound_analysis.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    '''
    connection.execute(
        "INSERT INTO images(filename)"
        "VALUES(?)", (uuid_basename,)
    )'''
    return {"filename": uuid_basename}
    

@wound_analysis.app.route('/download/<path:filename>')
def download_file(filename):
    return flask.send_from_directory("",
                                     filename, as_attachment=True)

# [END gae_python38_app]
