import React from "react";
import TextField from "@material-ui/core/TextField";
import style from "./style.js";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(style);

function MaskSelector(props) {
  const classes = useStyles();
  return (
    <div>
      <TextField
        label="Lower Range"
        className={classes.textField}
        valueLower={props.lowerMask}
        placeholder={"10,10,10"}
        onChange={props.onChangeLower}
        margin="normal"
      />
      <TextField
        label="Upper Range"
        className={classes.textField}
        valueUpper={props.upperMask}
        placeholder={"10,10,10"}
        onChange={props.onChangeUpper}
        margin="normal"
      />
    </div>
  );
}

export default MaskSelector;
