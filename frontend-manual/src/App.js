import React, { useState, useEffect } from 'react';
// plugin that creates slider
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
// core components
import Button from "./components/CustomButtons/Button.js";
import CustomInput from "./components/CustomInput/CustomInput.js";

import styles from "assets/jss/material-kit-react/views/componentsSections/basicsStyle.js";
import "./style.css";
const useStyles = makeStyles(styles);


function App() {
  const [currentImage, setCurrentImage] = useState();
  const [testText, setTestText] = useState("default");
  const [currentTime, setCurrentTime] = useState(0);
  const classes = useStyles();

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  const onImageChange = event => {
    if (event.target.files && event.target.files[0]) {
      let img = event.target.files[0];
      setCurrentImage(URL.createObjectURL(img));
    }
  };

  const analyzeImage = async (event) => {
    setTestText("tested!")
    const formData = new FormData()

    formData.append("image", currentImage)
    setTestText("tested21!")  
    
    await fetch("/recog/", {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      setCurrentImage(data)
    })
  }

  return (
    <div className={classes.sections}>
      <div className={classes.container}>
        <div className={classes.title}>
          <h2>Automatic Wound Area Measurement</h2>
        </div>
        <div class="row">
          <div class="column">
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
              />
            </div>
          </div>
          <div class="column">
            <h3>Image</h3>
            <img src={currentImage} style={{width: "100%", flex: 1}} />
          </div>
        </div>
      
        <h3>{testText}</h3>
        <p>The current time is {currentTime}.</p>
        
        <Button color="primary" onClick={analyzeImage}>Measure area</Button>
      </div>
    </div>
  );
}


export default App;
