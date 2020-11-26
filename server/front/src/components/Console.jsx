// Third party
import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';

const nullish = [null, undefined];

export const Console = () => {
  const { state } = window;

  const doLogout = () => {
    window.location.assign('/')
  };

  // Redirect to index as there is no state to work from
  if (nullish.includes(state) || nullish.includes(state.email)) {
    doLogout()
  }

  return (
    <React.StrictMode>
      <CssBaseline />
      <h1>Welcome {state.email}!!</h1>

      <button onClick={doLogout}>Logout</button>
    </React.StrictMode>
  );
}
