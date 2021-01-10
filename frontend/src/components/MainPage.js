import React, { useState } from "react";
import Cropper from "./ImageCropper/imageCropper";
import Button from "@material-ui/core/Button";

import CustomInput from "components/CustomInput/CustomInput.js";
import styles from "./style.js";
import classNames from "classnames";
import { withStyles } from "@material-ui/core/styles";

import MaskSelector from "./MaskSelector/index.js";

class MainPage extends React.Component {
  state = {
    currentImage: null,
    currentImageFile: null,
    analyzed: false,
    imageWidth: null,
    useCrop: false,
    areas: [],
    lowerMask: null,
    uppperMask: null,
  };

  completeCrop = (image, imageFile) => {
    this.setState({
      useCrop: false,
      currentImage: image,
      currentImageFile: imageFile,
    });
  };

  onImageChange = (event) => {
    console.log("image changed");
    if (event.target.files && event.target.files[0]) {
      let imgFile = event.target.files[0];
      this.setState({
        currentImage: URL.createObjectURL(imgFile),
        currentImageFile: imgFile,
      });
    }
  };

  analyzeImage = async (event) => {
    event.preventDefault();
    if (this.state.currentImage && this.state.imageWidth) {
      const url = "/analyze/";
      const form = new FormData();
      console.log("analyzeImage");
      console.log(this.state.currentImageFile);
      form.append("file", this.state.currentImageFile);
      form.append("mode", "run");
      form.append("width", this.state.imageWidth);

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
          this.setState({
            analyzed: true,
            currentImage: data["drawn_image"],
            areas: data.areas,
          });
        })
        .catch((error) => console.log(error));
    } else if (this.state.currentImage && !this.state.imageWidth) {
      alert("Please specify an image width");
    } else if (!this.state.currentImage && this.state.imageWidth) {
      alert("Please upload an image");
    } else {
      alert("Please upload an image and specify it's real width");
    }
  };

  handleOnChange = (event) => {
    this.setState({
      imageWidth: event.target.value,
    });
  };

  handleCropChange = () => {
    this.setState({
      useCrop: true,
    });
  };

  handleLowerMaskChange = (lowerMask) => {
    this.setState({
      lowerMask: lowerMask,
    });
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div className={classes.container}>
          <MaskSelector
            valueLower={this.state.lowerMask}
            onChangeLower={this.handleLowerMaskChange}
          />
          <div className={classes.title}>
            <h2>Automatic Wound Area Measurement</h2>
          </div>
          <div className={classes.row}>
            <div className={classes.column}>
              <div className={classes.button} style={{ flex: 1 }}>
                <h3>Upload Image</h3>
                <input
                  type="file"
                  name="myImage"
                  onChange={this.onImageChange}
                />
              </div>
              <div style={{ width: "25%", flex: 1 }}>
                <CustomInput
                  labelText="Enter real image width"
                  id="float"
                  formControlProps={{
                    fullWidth: true,
                  }}
                  inputProps={{
                    onChange: this.handleOnChange,
                  }}
                />
              </div>
            </div>
            <div className={classes.column}>
              <h3>Image</h3>
              {this.state.useCrop ? (
                <Cropper
                  currentImage={this.state.currentImage}
                  completeCrop={this.completeCrop}
                />
              ) : this.state.currentImage && !this.state.analyzed ? (
                <div className={classes.column}>
                  <img
                    src={this.state.currentImage}
                    className={classes.images}
                    alt=""
                  />
                  <Button
                    className={classes.cropButton}
                    variant="contained"
                    color="primary"
                    onClick={this.handleCropChange}
                  >
                    Crop Image
                  </Button>
                </div>
              ) : this.state.analyzed ? (
                <img
                  src={"data:image/png;base64," + this.state.currentImage}
                  className={classes.images}
                  alt=""
                />
              ) : null}
            </div>
          </div>
          <h3>Areas:</h3>
          {this.state.areas.map((value) => (
            <p>{value} u^2</p>
          ))}

          <Button
            variant="contained"
            color="primary"
            onClick={this.analyzeImage}
          >
            Measure area
          </Button>
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(MainPage);
