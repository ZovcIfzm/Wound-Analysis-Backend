
# [START gae_python38_app]
import flask
import os
import cv2
import time
import requests

import numpy as np
import json
import wound_analysis
from PIL import Image

import io
import base64

import zipfile

import wound_analysis.api.analysis as analysis
import wound_analysis.api.helpers as helpers
import wound_analysis.api.constants as k

from flask_cors import CORS, cross_origin
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
from flask import current_app

@wound_analysis.app.route('/time/')
def get_current_time():
    return {'time': time.time()}

@wound_analysis.app.route('/zipMeasure', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def zipMeasure():
    
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    archive = zipfile.ZipFile(fileobj, 'r')
    namelist = archive.namelist()

    width = float(flask.request.form.get("width"))
    
    image_list = []
    for img_name in namelist:
        imgfile = archive.open(img_name)

        # Convert image file to opencv format
        image = Image.open(imgfile)
        buf = io.BytesIO()
        image.save(buf, 'jpeg')
        buf.seek(0)
        image_bytes = buf.read()
        buf.close()

        base64_bytes = base64.b64encode(image_bytes)
        decoded = base64_bytes.decode()
        input_base64_image = "data:image/jpeg;base64," + decoded
        
        pil_image = image.convert('RGB') 
        opencv_image = np.array(pil_image) 

        # Convert RGB to BGR 
        opencv_image = opencv_image[:, :, ::-1].copy() 
        
        small_to_large_image_size_ratio = 0.25
        opencv_image = cv2.GaussianBlur(opencv_image, (3, 3), cv2.BORDER_DEFAULT)
        opencv_image = cv2.resize(opencv_image, # original image
                                (0,0), # set fx and fy, not the final size
                                fx=small_to_large_image_size_ratio, 
                                fy=small_to_large_image_size_ratio, 
                                interpolation=cv2.INTER_NEAREST)

        # Select mask
        manual_mask = flask.request.form.get("manual_mask")
        manual_mask = True if manual_mask == "true" else False
        
        lower_mask_one, lower_mask_two, upper_mask_one, upper_mask_two = None, None, None, None
        print("DEBUG: manual_mask", manual_mask)

        if manual_mask:
            print("DEBUG: manual_mask not run")
            lower_mask_one = helpers.convertStringToNumpyArray(str(flask.request.form.get("lower_mask_one")))
            lower_mask_two = helpers.convertStringToNumpyArray(str(flask.request.form.get("lower_mask_two")))
            upper_mask_one = helpers.convertStringToNumpyArray(str(flask.request.form.get("upper_mask_one")))
            upper_mask_two = helpers.convertStringToNumpyArray(str(flask.request.form.get("upper_mask_two")))
        else:
            print("DEBUG: manual_mask run")
            mask_list = [(k.A_LR, k.A_UR), (k.B_LR, k.B_UR), (k.C_LR, k.C_UR), (k.D_LR, k.D_UR), (k.E_LR, k.E_UR)]
            obj = {"b64img": decoded}
            predicted_mask = int(requests.post(k.ML_API, json=obj).text)
            print("predicted mask", predicted_mask)
            #predicted_mask = siamese.predict(image, current_app.config["MODEL_PATH"])
            lower_mask_one = mask_list[predicted_mask][0][0]
            lower_mask_two = mask_list[predicted_mask][0][1]
            upper_mask_one = mask_list[predicted_mask][1][0]
            upper_mask_two = mask_list[predicted_mask][1][1]
            print("DEBUG: manual_mask predicted mask = ", predicted_mask)

        mask_map = {
            "lower_range": {
                "first": lower_mask_one,
                "second": lower_mask_two
            },
            "upper_range": {
                "first": upper_mask_one,
                "second": upper_mask_two
            }
        }

        obj = analysis.zip_measurement(opencv_image, mask_map, width=width)
        obj["orig"] = input_base64_image
        image_list.append(obj)

    response = json.dumps(image_list)
    return response

@wound_analysis.app.route('/measure', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def measure():
    # Retrieve fields
    width = float(flask.request.form.get("width"))
    
    input_base64_image = flask.request.form.get("base64")
    b64_string = input_base64_image.split("data:image/jpeg;base64")[1]
    manual_width = flask.request.form.get("manual_width")
    manual_mask = flask.request.form.get("manual_mask")

    print("DEBUG: raw manual_mask:", manual_mask)
    print("DEBUG: raw manual_width:", manual_width)
    manual_width = True if manual_width == "true" else False
    manual_mask = True if manual_mask == "true" else False

    # Convert image file to opencv format
    decoded = base64.b64decode(b64_string)
    ioed = io.BytesIO(decoded)
    image = Image.open(ioed)
    pil_image = image.convert('RGB') 
    opencv_image = np.array(pil_image) 

    # Convert RGB to BGR 
    opencv_image = opencv_image[:, :, ::-1].copy() 
    
    small_to_large_image_size_ratio = 0.25
    opencv_image = cv2.GaussianBlur(opencv_image, (3, 3), cv2.BORDER_DEFAULT)
    opencv_image = cv2.resize(opencv_image, # original image
                            (0,0), # set fx and fy, not the final size
                            fx=small_to_large_image_size_ratio, 
                            fy=small_to_large_image_size_ratio, 
                            interpolation=cv2.INTER_NEAREST)
    lower_mask_one, lower_mask_two, upper_mask_one, upper_mask_two = None, None, None, None
    print("DEBUG: manual_mask", manual_mask)
    # Find mask
    if manual_mask:
        print("DEBUG: manual_mask not run")
        lower_mask_one = helpers.convertStringToNumpyArray(str(flask.request.form.get("lower_mask_one")))
        lower_mask_two = helpers.convertStringToNumpyArray(str(flask.request.form.get("lower_mask_two")))
        upper_mask_one = helpers.convertStringToNumpyArray(str(flask.request.form.get("upper_mask_one")))
        upper_mask_two = helpers.convertStringToNumpyArray(str(flask.request.form.get("upper_mask_two")))
    else:
        print("DEBUG: manual_mask run")
        mask_list = [(k.A_LR, k.A_UR), (k.B_LR, k.B_UR), (k.C_LR, k.C_UR), (k.D_LR, k.D_UR), (k.E_LR, k.E_UR)]
        obj = {"b64img": b64_string}
        predicted_mask = int(requests.post(k.ML_API, json=obj).text)
        print("predicted mask", predicted_mask)
        #predicted_mask = siamese.predict(image, current_app.config["MODEL_PATH"])
        lower_mask_one = mask_list[predicted_mask][0][0]
        lower_mask_two = mask_list[predicted_mask][0][1]
        upper_mask_one = mask_list[predicted_mask][1][0]
        upper_mask_two = mask_list[predicted_mask][1][1]
        print("DEBUG: manual_mask predicted mask = ", predicted_mask)

    mask_map = {
        "lower_range": {
            "first": lower_mask_one,
            "second": lower_mask_two
        },
        "upper_range": {
            "first": upper_mask_one,
            "second": upper_mask_two
        }
    }

    data_matrix = analysis.grid_measurement(opencv_image, mask_map, manual=manual_width, width=width)
    for row in data_matrix:
        for col in row:
            col["orig"] = input_base64_image

    response = json.dumps(data_matrix)
    return response


@wound_analysis.app.route('/testImage', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def testImage():

    # Retrieve fields
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    # Convert image file to opencv format
    pil_image = Image.open(fileobj).convert('RGB') 
    opencv_image = np.array(pil_image) 

    # Convert RGB to BGR 
    opencv_image = opencv_image[:, :, ::-1].copy() 

    response = json.dumps(helpers.convertNumpyImageToString(opencv_image))
    #print(response)
    return response

@wound_analysis.app.route('/', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def hello():
    """Return a friendly HTTP greeting."""
    return "This is the wound analysis api"

@wound_analysis.app.route('/imageSend', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def imageSend():
    
    input_base64_image = flask.request.form.get("base64")
    b64_string = input_base64_image.split("data:image/jpeg;base64")[1]

    response = requests.post("localhost:5000", data={"b64img": b64_string})
    print("response:", response)
    return response