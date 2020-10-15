import React, { useState, useEffect } from 'react';
// plugin that creates slider
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
// core components
import Button from "components/CustomButtons/Button.js";
import CustomInput from "components/CustomInput/CustomInput.js";

import styles from "assets/jss/material-kit-react/views/componentsSections/basicsStyle.js";
import "./style.css";
const useStyles = makeStyles(styles);

export default function SectionBasics() {
  const [currentImage, setCurrentImage] = useState();
  const [currentImageFilename, setCurrentImageFilename] = useState();
  const [analyzed, setAnalyzed] = useState(0);
  const [imageWidth, setImageWidth] = useState();
  const [testText, setTestText] = useState("default");
  const classes = useStyles();
  
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time/').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  const onImageChange = event => {
    if (event.target.files && event.target.files[0]) {
      let img = event.target.files[0];
      console.log(img)
      setCurrentImage(URL.createObjectURL(img));
      const form = new FormData();
      form.append('file', img);
      const url = "/upload/"
      const options = {
        method: 'POST',
        body: form,
      };
      fetch(url, options)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json()
        })
        .then((data) => {
          console.log("dataOnImageChange:, ", data)
          setCurrentImageFilename(data.filename)
        })
        .catch((error) => console.log(error));
    }
  };

  const analyzeImage = async (event) => {
    event.preventDefault();
    console.log("curF: ", currentImageFilename)
    if (currentImageFilename && imageWidth) {
      const url = "/analyze/"
      const form = new FormData();
      form.append('filename', currentImageFilename);
      form.append('mode', "run")
      form.append("width", imageWidth)
      console.log("cur: ", currentImageFilename)
      const options = {
        method: 'POST',
        body: form,
      };
      fetch(url, options)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json()
        })
        .then((data) => {
          console.log("in data2")
          console.log(data)
          setAnalyzed(data.analyzed)
        })
        .catch((error) => console.log(error));
    }
    else if (currentImageFilename && !imageWidth) {
      alert("Please specify an image width")
    }
    else if (!currentImageFilename && imageWidth) {
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
            {currentImage && !analyzed ? 
            <img src={currentImage} style={{width: "100%", flex: 1}} alt="" />
            : null}
            {analyzed ? 
            <img src={"../../../../../../database/uploads/analyzed.png"} style={{width: "100%", flex: 1}} alt="" />
            : null}
          </div>
        </div>
        
        <h3>{testText}</h3>
        <p>The current time is {currentTime}.</p>
        
        <Button color="success" onClick={analyzeImage}>Measure area</Button>
      </div>
    </div>
  );
}
