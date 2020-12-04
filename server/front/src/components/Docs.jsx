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
import { THEME } from '../utils/theme';

const useStyles = makeStyles((theme) => ({
}));

export const Docs = ({ bigScreen }) => {
  const classes = useStyles();

  return (
    <React.Fragment>
      <div className={classes.root}>
        <SnackbarProvider maxSnack={3}>
          <Router basename="/docs">
            <br />
            <Switch>
            </Switch>
            <Copyright />
          </Router>
        </SnackbarProvider>
      </div>
    </React.Fragment>
  );
}
