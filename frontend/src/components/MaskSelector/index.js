import React from "react";
import TextField from "@material-ui/core/TextField";
import style from "./style.js";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(style);

function MaskSelector(props) {
  const classes = useStyles();
  const placeholder = "hue, sat, val";
  return (
    <div className={classes.row}>
      <div className={classes.column}>
        <div className={classes.row}>
          <TextField
            label="HSV Lower Range 1"
            className={classes.textField}
            value={props.lowerMaskOne}
            placeholder={placeholder}
            onChange={props.onChangeLowerOne}
            margin="normal"
          />
          <TextField
            label="HSV Lower Range 2"
            className={classes.textField}
            value={props.lowerMaskTwo}
            placeholder={placeholder}
            onChange={props.onChangeLowerTwo}
            margin="normal"
          />
        </div>
        <div className={classes.row}>
          <TextField
            label="HSV Upper Range 1"
            className={classes.textField}
            value={props.upperMaskOne}
            placeholder={placeholder}
            onChange={props.onChangeUpperOne}
            margin="normal"
          />
          <TextField
            label="HSV Upper Range 2"
            className={classes.textField}
            value={props.upperMaskTwo}
            placeholder={placeholder}
            onChange={props.onChangeUpperTwo}
            margin="normal"
          />
        </div>
      </div>
      <div className={classes.column}>
        <div>Lower Mask One C</div>
        <div>0, 100, 20</div>
      </div>
      <div className={classes.column}>
        <div>Lower Mask Two C</div>
        <div>150, 100, 20</div>
      </div>
      <div className={classes.column}>
        <div>Upper Mask One C</div>
        <div>30, 255, 177</div>
      </div>
      <div className={classes.column}>
        <div>Upper Mask Two C</div>
        <div>180, 255, 177</div>
      </div>
    </div>
  );
}

export default MaskSelector;
