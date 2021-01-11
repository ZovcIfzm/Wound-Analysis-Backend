import React from "react";
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
    edgedImage: null,
    analyzed: false,
    imageWidth: null,
    useCrop: false,
    areas: [],
    lowerMaskOne: "0, 100, 20",
    lowerMaskTwo: "150, 100, 20",
    upperMaskOne: "30, 255, 177",
    upperMaskTwo: "180, 255, 177",
  };

  completeCrop = (image, imageFile) => {
    this.setState({
      useCrop: false,
      currentImage: image,
      currentImageFile: imageFile,
    });
  };

  onImageChange = (event) => {
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
      const url = "/measure";
      const form = new FormData();
      form.append("file", this.state.currentImageFile);
      form.append("mode", "run");
      form.append("width", this.state.imageWidth);
      console.log(this.state.lowerMaskOne);
      form.append("lower_mask_one", this.state.lowerMaskOne);
      form.append("lower_mask_two", this.state.lowerMaskTwo);
      form.append("upper_mask_one", this.state.upperMaskOne);
      form.append("upper_mask_two", this.state.upperMaskTwo);

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
          this.setState({
            analyzed: true,
            currentImage: data["drawn_image"],
            edgedImage: data["edged_image"],
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

  handleLowerMaskOneChange = (event) => {
    this.setState({
      lowerMaskOne: event.target.value,
    });
  };

  handleLowerMaskTwoChange = (event) => {
    this.setState({
      lowerMaskTwo: event.target.value,
    });
  };

  handleUpperMaskOneChange = (event) => {
    this.setState({
      upperMaskOne: event.target.value,
    });
  };

  handleUpperMaskTwoChange = (event) => {
    this.setState({
      upperMaskTwo: event.target.value,
    });
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div className={classes.container}>
          <MaskSelector
            lowerMaskOne={this.state.lowerMaskOne}
            lowerMaskTwo={this.state.lowerMaskTwo}
            upperMaskOne={this.state.upperMaskOne}
            upperMaskTwo={this.state.upperMaskTwo}
            onChangeLowerOne={this.handleLowerMaskOneChange.bind(this)}
            onChangeLowerTwo={this.handleLowerMaskTwoChange.bind(this)}
            onChangeUpperOne={this.handleUpperMaskOneChange.bind(this)}
            onChangeUpperTwo={this.handleUpperMaskTwoChange.bind(this)}
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
                <>
                  <h4>Image with border</h4>
                  <img
                    src={"data:image/png;base64," + this.state.currentImage}
                    className={classes.images}
                    alt=""
                  />
                  <h4>Border generated</h4>
                  <img
                    src={"data:image/png;base64," + this.state.edgedImage}
                    className={classes.images}
                    alt=""
                  />
                </>
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
