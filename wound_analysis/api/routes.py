
# [START gae_python38_app]
import flask
import os
from werkzeug.utils import secure_filename
import cv2
import time

import wound_analysis

from wound_analysis.api.area_optimization import default_measurement, optimized_masking_measurement, manual_area_adjustment
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.

global test_val
test_val = 0
global data
data = {}


@wound_analysis.app.route('/time')
def get_current_time():
    return {'time': time.time()}


@wound_analysis.app.route('/post/', methods=['POST', 'GET'])
def post():
    print("reached post")
    fileobj = flask.request.files["file"]

    fileobj.save(os.path.join(app.root_path, "cur_image.jpg"))
    print("post saved")
    return flask.redirect("/")


@wound_analysis.app.route('/testPrint', methods=['POST', 'GET'])
def show_time():
    print("tested")
    response = {"test": "testedInFlask"}
    return flask.make_response(flask.jsonify(response))


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


@wound_analysis.app.route('/uploads/<path:filename>')
def download_file(filename):
    return flask.send_from_directory("",
                                     filename, as_attachment=True)

# [END gae_python38_app]
