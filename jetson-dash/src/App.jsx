import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [frame, setFrame] = useState("");


  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8080");

    ws.onopen = () => {
      console.log("Websocket connected");
    };

    ws.onmessage = (event) => {
      setFrame(`data:image/jpeg;base64, ${event.data}`);
    };

    ws.onerror = (error) => {
      console.error("Websocket error: ", error);
    };

    ws.onclose = () => {
      console.log("Websocket disconnected");
    };
  },);

  return (
  <>
    <h1>Jetson Dash</h1>
    <h2>Live Video Feed</h2>
    {(frame) ?  (<img src = {frame}/>) : (<h3>Loading...</h3>)}
  </>
);
}

export default App;
