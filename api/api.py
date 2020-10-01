# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
import flask
import os
from werkzeug.utils import secure_filename
import cv2

from area_optimization import default_measurement, optimized_masking_measurement, manual_area_adjustment
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
global test_val
test_val = 0
global data
data = {}


@app.route('/post/', methods=['POST', 'GET'])
def post():
    print("reached post")
    fileobj = flask.request.files["file"]

    fileobj.save(os.path.join(app.root_path, "cur_image.jpg"))
    print("post saved")
    return flask.redirect("/")


@app.route('/time')
def show_time():
    return {"time": 4}


@app.route('/recog/', methods=['POST', 'GET'])
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


@ app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return flask.render_template("index.html")


@ app.route('/uploads/<path:filename>')
def download_file(filename):
    return flask.send_from_directory("",
                                     filename, as_attachment=True)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
