// Third party
import { SnackbarProvider } from 'notistack';
import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import {
  CssBaseline,
} from '@material-ui/core';

// Local libraries
import { useStylesConsole } from '../classes';
import { CachIPFS } from './CachIPFS';
import { Copyright } from './Copyright';
import { ConsoleAppBar } from './ConsoleAppBar';

// Constants
const nullish = [null, undefined];

export const Console = () => {
  const classes = useStylesConsole();
  const { state } = window;

  // Redirect to index as there is no state to work from
  if (nullish.includes(state) || nullish.includes(state.email)) {
    doLogout()
  }

  return (
    <React.StrictMode>
      <CssBaseline />
      <div className={classes.root}>
        <SnackbarProvider maxSnack={3}>
          <Router basename="/console">
            <ConsoleAppBar />
            <Switch>
              <Route path="/cachipfs" component={CachIPFS} />
              <Redirect to="/cachipfs" />
            </Switch>
            <Copyright />
          </Router>
        </SnackbarProvider>
      </div>
    </React.StrictMode>
  );
}
