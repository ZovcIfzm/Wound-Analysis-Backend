import React, { useState, useEffect, useCallback} from 'react';
import Cropper from 'react-easy-crop'
import Slider from '@material-ui/core/Slider'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import getCroppedImg from './cropImage'

import { makeStyles } from "@material-ui/core/styles";

import CustomInput from "components/CustomInput/CustomInput.js";


import styles from "assets/jss/material-kit-react/views/componentsSections/basicsStyle.js";
import "./style.css";
const useStyles = makeStyles(styles);

export default function SectionBasics() {
  const [currentImage, setCurrentImage] = useState();
  const [currentImageFile, setCurrentImageFile] = useState();
  const [currentImageFilename, setCurrentImageFilename] = useState();
  const [analyzed, setAnalyzed] = useState(0);
  const [imageWidth, setImageWidth] = useState();
  const [useCrop, setUseCrop] = useState(0)
  const classes = useStyles();
  const [currentTime, setCurrentTime] = useState(0);
  const [areas, setAreas] = useState([]);

  //For Cropper
  const [crop, setCrop] = useState({ x: 0, y: 0 })
  const [rotation, setRotation] = useState(0)
  const [zoom, setZoom] = useState(1)
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null)

  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels)
  }, [])

  const showCroppedImage = useCallback(async () => {
    try {
      const croppedImage = await getCroppedImg(
        currentImage,
        croppedAreaPixels,
        rotation
      )
      setCurrentImage(croppedImage)
      setUseCrop(false)
      /*
      fetch(croppedImage).then(function(response) {
        return response.blob();
      }).then(function(myBlob) {
        let sendFile = new File([myBlob], currentImageFilename, {type: "image/jpeg", lastModified: Date.now()});
        uploadImage(sendFile)
      })*/
    } catch (e) {
      console.error(e)
    }
  }, [currentImage, croppedAreaPixels, rotation])

  //Normal code
  useEffect(() => {
    fetch('/time/').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  const onImageChange = event => {
    if (event.target.files && event.target.files[0]) {
      let imgFile = event.target.files[0];
      setCurrentImageFile(imgFile)
      setCurrentImage(URL.createObjectURL(imgFile));
    }
  };

  const analyzeImage = async (event) => {
    event.preventDefault();
    if (currentImage && imageWidth) {
      const url = "/analyze/"
      const form = new FormData();      
      console.log("currentImageFile: ", currentImageFile)
      form.append('file', currentImageFile);
      form.append('mode', "run")
      form.append("width", imageWidth)
      
      //Then analyze
      const analyze_options = {
        method: 'POST',
        body: form,
      };
      fetch(url, analyze_options)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json()
        })
        .then((data) => {
          //setAnalyzedUrl(`http://localhost:5000/uploads/${data.url}`)
          console.log("analyzed: ", data["drawn_image"])
          setAnalyzed(true)
          setCurrentImage(data["drawn_image"])
          setAreas(data.areas)
        })
        .catch((error) => console.log(error));
    }
    else if (currentImage && !imageWidth) {
      alert("Please specify an image width")
    }
    else if (!currentImage && imageWidth) {
      alert("Please upload an image")
    }
    else{
      alert("Please upload an image and specify it's real width")
    }
  }

  const handleOnChange = (event) => {
    setImageWidth(event.target.value)
  }

  return (
    <div className={classes.sections}>
      <div className={classes.container}>
        <div className={classes.title}>
          <h2>Automatic Wound Area Measurement</h2>
        </div>
        <div className="row">
          <div className="column">
            <div className='button' style={{flex: 1}}>
              <h3>Upload Image</h3>
              <input type="file" name="myImage" onChange={onImageChange} />
            </div>
            <div style={{width:"25%", flex: 1}}>
              <CustomInput
                labelText="Enter real image width"
                id="float"
                formControlProps={{
                  fullWidth: true
                }}
                inputProps={{
                  onChange: handleOnChange
                }}
              />
            </div>
          </div>
          <div className="column">
            <h3>Image</h3>
            {useCrop ? 
            <div>
              <div style={{position: 'relative',
                width: '100%',
                height: 200,
                background: '#333',
                }}>
                <Cropper
                  image={currentImage}
                  crop={crop}
                  rotation={rotation}
                  zoom={zoom}
                  aspect={3 / 3}
                  onCropChange={setCrop}
                  onRotationChange={setRotation}
                  onCropComplete={onCropComplete}
                  onZoomChange={setZoom}
                />
              </div>
              <div>
                <div>
                  <Typography
                    variant="overline"
                  >
                    Zoom
                  </Typography>
                  <Slider
                    value={zoom}
                    min={1}
                    max={3}
                    step={0.01}
                    aria-labelledby="Zoom"
                    onChange={(e, zoom) => setZoom(zoom)}
                  />
                </div>
                <div>
                  <Typography
                    variant="overline"
                  >
                    Rotation
                  </Typography>
                  <Slider
                    value={rotation}
                    min={0}
                    max={360}
                    step={0.01}
                    aria-labelledby="Rotation"
                    onChange={(e, rotation) => setRotation(rotation)}
                  />
                </div>
                <Button
                  onClick={showCroppedImage}
                  variant="contained"
                  color="primary"
                >
                  Crop Image
                </Button>
              </div>
            </div>
            : currentImage && !analyzed ? 
            
            <div>
              <img src={currentImage} style={{width: "100%", flex: 1}} alt="" />
              <Button variant="contained" color="primary" onClick={() => setUseCrop(true)}>Crop Image</Button>
            </div>
            
            : analyzed ? 
            <img src={"data:image/png;base64," +  currentImage} style={{width: "100%", flex: 1}} alt="" />
            : null}
          </div>
        </div>
        <h3>Areas:</h3>
        {
          areas.map((value) => (<p>{value} u^2</p>))
        }        
        
        <Button variant="contained" color="primary" onClick={analyzeImage}>Measure area</Button>
      </div>
    </div>
  );
}

