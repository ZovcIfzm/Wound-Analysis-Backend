import React from "react";
import logo from "./logo.svg";
import "./App.css";

class App extends React.Component {
  state = {
    currentTime: 0,
    currentTime2: 0,
    imgData: null
  };

  doTheThing = () => {
    fetch("/time")
      .then((res) => res.json())
      .then((data) => {
        setCurrentTime(data.time);
      });
    fetch("/api/time")
      .then((res) => res.json())
      .then((data) => {
        setCurrentTime2(data.time);
      });
  };

  toggleTouched = () => {
    this.setState((prevState) => ({
      touched: !prevState.touched
    }));
  };

  handleMouseUp = () => {
    // Handle smooth animation when clicking without holding
    setTimeout(() => {
      this.setState({ touched: false });
    }, 150);
  };
  render() {
    return (
      <div className="App">
        <header className="App-header">
          ... no changes in this part ...
          <p>The current time is {currentTime}.</p>
          <p>The current time is {currentTime2}.</p>
        </header>
        {imgData ? <img src={`data:image/png;base64,${imgData}`} /> : ""}
        <button onMouseDown={this.toggleTouched} onMouseUp={this.handleMouseUp}>
          Touch Here
        </button>
        <button onMouseDown={this.doTheThing}>Touch Here 2</button>
      </div>
    );
  }
}

export default App;
