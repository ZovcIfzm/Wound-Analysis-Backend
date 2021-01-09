import React, { useState } from "react";
import Cropper from "./ImageCropper/imageCropper";
import Button from "@material-ui/core/Button";

import CustomInput from "components/CustomInput/CustomInput.js";
import style from "./style.js";
import classNames from "classnames";
import { makeStyles } from "@material-ui/core/styles";
const useStyles = makeStyles(style);

export default function MainPage() {
  const [currentImage, setCurrentImage] = useState();
  const [currentImageFile, setCurrentImageFile] = useState();
  const [analyzed, setAnalyzed] = useState(0);
  const [imageWidth, setImageWidth] = useState();
  const [useCrop, setUseCrop] = useState(0);
  const [areas, setAreas] = useState([]);

  const styles = useStyles();

  const completeCrop = (image) => {
    setUseCrop(false);
    setCurrentImage(image);
  };

  const onImageChange = (event) => {
    console.log("image changed");
    if (event.target.files && event.target.files[0]) {
      let imgFile = event.target.files[0];
      setCurrentImageFile(imgFile);
      setCurrentImage(URL.createObjectURL(imgFile));
    }
  };

  const analyzeImage = async (event) => {
    event.preventDefault();
    if (currentImage && imageWidth) {
      const url = "/analyze/";
      const form = new FormData();
      form.append("file", currentImageFile);
      form.append("mode", "run");
      form.append("width", imageWidth);

      //Then analyze
      const analyze_options = {
        method: "POST",
        body: form,
      };
      fetch(url, analyze_options)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          //setAnalyzedUrl(`http://localhost:5000/uploads/${data.url}`)
          console.log("analyzed: ", data["drawn_image"]);
          setAnalyzed(true);
          setCurrentImage(data["drawn_image"]);
          setAreas(data.areas);
        })
        .catch((error) => console.log(error));
    } else if (currentImage && !imageWidth) {
      alert("Please specify an image width");
    } else if (!currentImage && imageWidth) {
      alert("Please upload an image");
    } else {
      alert("Please upload an image and specify it's real width");
    }
  };

  const handleOnChange = (event) => {
    setImageWidth(event.target.value);
  };

  return (
    <div className={classNames(styles.main, styles.mainRaised)}>
      <div className={styles.sections}>
        <div className={styles.container}>
          <div className={styles.title}>
            <h2>Automatic Wound Area Measurement</h2>
          </div>
          <div className={styles.row}>
            <div className={styles.column}>
              <div className={styles.button} style={{ flex: 1 }}>
                <h3>Upload Image</h3>
                <input type="file" name="myImage" onChange={onImageChange} />
              </div>
              <div style={{ width: "25%", flex: 1 }}>
                <CustomInput
                  labelText="Enter real image width"
                  id="float"
                  formControlProps={{
                    fullWidth: true,
                  }}
                  inputProps={{
                    onChange: handleOnChange,
                  }}
                />
              </div>
            </div>
            <div className={styles.column}>
              <h3>Image</h3>
              {useCrop ? (
                <Cropper
                  currentImage={currentImage}
                  completeCrop={completeCrop}
                />
              ) : currentImage && !analyzed ? (
                <div className={styles.column}>
                  <img src={currentImage} className={styles.test} alt="" />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => setUseCrop(true)}
                  >
                    Crop Image
                  </Button>
                </div>
              ) : analyzed ? (
                <img
                  src={"data:image/png;base64," + currentImage}
                  style={{ width: 200 }}
                  alt=""
                />
              ) : null}
            </div>
          </div>
          <h3>Areas:</h3>
          {areas.map((value) => (
            <p>{value} u^2</p>
          ))}

          <Button variant="contained" color="primary" onClick={analyzeImage}>
            Measure area
          </Button>
        </div>
      </div>
    </div>
  );
}
