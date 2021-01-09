// You can choose your kind of history here (e.g. browserHistory)
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import MainPage from "./components/MainPage";
require("typeface-roboto-slab");
// Your routes.js file

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route path="/" component={MainPage} exact />
    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
);
