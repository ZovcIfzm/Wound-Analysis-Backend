
# [START gae_python38_app]
import flask
import os
from werkzeug.utils import secure_filename
import cv2
import time

import pathlib
import uuid

import numpy as np
import json
import wound_analysis
from PIL import Image
import pickle

import wound_analysis.api.analysis as analysis
import wound_analysis.api.helpers as helpers
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.

global test_val
test_val = 0
global data
data = {}

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

@wound_analysis.app.route('/measure', methods=['POST', 'GET'])
def measure():
    global data
    global test_val

    # Retrieve fields
    width = float(flask.request.form.get("width"))
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    lower_mask_one = str(flask.request.form.get("lower_mask_one"))
    lower_mask_two = str(flask.request.form.get("lower_mask_two"))
    upper_mask_one = str(flask.request.form.get("upper_mask_one"))
    upper_mask_two = str(flask.request.form.get("upper_mask_two"))
    mask_map = {
        "lower_range": {
            "first": helpers.convertStringToNumpyArray(lower_mask_one),
            "second": helpers.convertStringToNumpyArray(lower_mask_two)
        },
        "upper_range": {
            "first": helpers.convertStringToNumpyArray(upper_mask_one),
            "second": helpers.convertStringToNumpyArray(upper_mask_two)
        }
    }

    # Convert image file to opencv format
    pil_image = Image.open(fileobj).convert('RGB') 
    opencv_image = np.array(pil_image) 

    # Convert RGB to BGR 
    opencv_image = opencv_image[:, :, ::-1].copy() 
    data_matrix = analysis.grid_measurement(opencv_image, width, mask_map)

    response = json.dumps(data_matrix)
    return response


@wound_analysis.app.route('/analyze/', methods=['POST', 'GET'])
def run_recog():
    global data
    global test_val
    mode = flask.request.form.get("mode")
    
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    pil_image = Image.open(fileobj).convert('RGB') 
    opencv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    opencv_image = opencv_image[:, :, ::-1].copy() 

    if mode == "run":
        width = float(flask.request.form.get("width"))
        image = opencv_image
        data = analysis.optimized_masking_measurement(image, width)
        _, im_arr = cv2.imencode('.jpg', data["drawn_image"])  # im_arr: image in Numpy one-dim array format.
        base64_bytes = base64.b64encode(im_arr)
        jpg_as_string = base64_bytes.decode('utf-8')
        drawn_image = jpg_as_string

        response = json.dumps({"drawn_image": drawn_image, "areas": data["areas"]})
        return response

    elif mode == "increase sat":
        width = float(flask.request.form.get("width"))
        data = analysis.manual_area_adjustment(data, True)
        print("printing data")
        # print(data)

        cv2.imwrite('cur_image.jpg', data["drawn_image"])
    elif mode == "decrease sat":
        width = float(flask.request.form.get("width"))
        data = analysis.manual_area_adjustment(data, False)
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

@wound_analysis.app.route('/uploads/<path:filename>', methods=['POST', 'GET'])
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
