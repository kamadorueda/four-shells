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
import {
  makeStyles,
  ThemeProvider,
} from '@material-ui/core/styles';

// Local libraries
import { Index as CachIPFSIndex } from './CachIPFS/Index';
import { Namespace as CachIPFSNamespace } from './CachIPFS/Namespace';
import { Copyright } from './Copyright';
import { ConsoleAppBar } from './ConsoleAppBar';
import { THEME } from '../theme';

// Constants
const nullish = [null, undefined];

const useStyles = makeStyles((theme) => ({
}));

export const Console = () => {
  const classes = useStyles();
  const { state } = window;

  // Redirect to index as there is no state to work from
  if (nullish.includes(state) || nullish.includes(state.email)) {
    doLogout()
  }

  return (
    <React.StrictMode>
      <CssBaseline />
      <ThemeProvider theme={THEME}>
        <div className={classes.root}>
          <SnackbarProvider maxSnack={3}>
            <Router basename="/console">
              <ConsoleAppBar />
              <br />
              <Switch>
                <Route path="/cachipfs/namespace/:id" component={CachIPFSNamespace} />
                <Route path="/cachipfs" component={CachIPFSIndex} />
                <Redirect to="/cachipfs" />
              </Switch>
              <Copyright />
            </Router>
          </SnackbarProvider>
        </div>
      </ThemeProvider>
    </React.StrictMode>
  );
}
