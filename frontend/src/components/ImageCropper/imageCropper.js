import React, { useState, useCallback } from "react";

import Cropper from "react-easy-crop";
import getCroppedImg from "./imageCropperHelper";

import Slider from "@material-ui/core/Slider";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";

export default function CustomCropper(props) {
  const currentImage = props.currentImage;
  const completeCrop = props.completeCrop;

  //For Cropper
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [rotation, setRotation] = useState(0);
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);

  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  const showCroppedImage = useCallback(async () => {
    try {
      const croppedImage = await getCroppedImg(
        currentImage,
        croppedAreaPixels,
        rotation
      );
      fetch(croppedImage)
        .then(function (response) {
          return response.blob();
        })
        .then(function (myBlob) {
          let croppedImageFile = new File([myBlob], "image", {
            type: "image/jpeg",
            lastModified: Date.now(),
          });
          completeCrop(croppedImage, croppedImageFile);
        });
    } catch (e) {
      console.error(e);
    }
  }, [completeCrop, currentImage, croppedAreaPixels, rotation]);

  return (
    <div>
      <div
        style={{
          position: "relative",
          width: "100%",
          height: 200,
          background: "#333",
        }}
      >
        <Cropper
          image={props.currentImage}
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
          <Typography variant="overline">Zoom</Typography>
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
          <Typography variant="overline">Rotation</Typography>
          <Slider
            value={rotation}
            min={0}
            max={360}
            step={0.01}
            aria-labelledby="Rotation"
            onChange={(e, rotation) => setRotation(rotation)}
          />
        </div>
        <Button onClick={showCroppedImage} variant="contained" color="primary">
          Crop Image
        </Button>
      </div>
    </div>
  );
}
