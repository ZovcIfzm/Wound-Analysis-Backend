import React from "react";
import { Route, Switch } from "react-router-dom";

import MainPage from "./components/MainPage";

export default function App() {
  return (
    <main>
      <Switch>
        <Route path="/" component={MainPage} exact />
      </Switch>
    </main>
  );
}
