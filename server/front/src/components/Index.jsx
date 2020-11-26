// Third party
import React from 'react';
import styled from 'styled-components';

export const Index = () => {
  const doLogin = () => {
    window.location.assign('/oauth/google/init')
  };

  return (
    <React.StrictMode>
      <h1>Welcome to Four Shells!!</h1>

      <button onClick={doLogin}>Login with Google</button>
    </React.StrictMode>
  );
}
