import React from 'react';
import ReactDOM from 'react-dom';

const Index = () => {
  return (
    <React.StrictMode>
      <h1>Welcome!!</h1>
    </React.StrictMode>
  );
}

ReactDOM.render(
  React.createElement(Index),
  document.getElementById("root"),
);
