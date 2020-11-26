// Third party
import React from 'react';
import styled from 'styled-components';

export const Dashboard = () => {
  const { state } = window;

  return (
    <React.StrictMode>
      <h1>Welcome {state.email}!!</h1>
    </React.StrictMode>
  );
}
