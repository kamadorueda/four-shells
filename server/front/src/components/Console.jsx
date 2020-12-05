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
  Container,
} from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';

// Local libraries
import { BarBreadcrumb } from './BarBreadcrumb';
import { BarMain } from './BarMain';
import { Index as CachIPFSIndex } from './CachIPFS/Index';
import { Namespace as CachIPFSNamespace } from './CachIPFS/Namespace';
import { Copyright } from './Copyright';

// Constants
const nullish = [null, undefined];

const formatEmail = (email) => {
  const username = email.split('@').slice(0, 1).join('');

  return `${username[0].toUpperCase()}${username.slice(1).toLowerCase()}`;
};

const useStyles = makeStyles((theme) => ({
}));

export const Console = ({ bigScreen }) => {
  const classes = useStyles();
  const { state } = window;

  // Redirect to index as there is no state to work from
  if (nullish.includes(state) || nullish.includes(state.email)) {
    doLogout()
  }

  return (
    <React.Fragment>
      <BarMain>
        {formatEmail(state.email)}'s Console
      </BarMain>
      <BarBreadcrumb />
      <Container maxWidth="lg">
        <SnackbarProvider maxSnack={3}>
          <Router basename="/console">
            <br />
            <Switch>
              <Route path="/cachipfs/namespace/:id" component={CachIPFSNamespace} />
              <Route path="/cachipfs" component={CachIPFSIndex} />
              <Redirect to="/cachipfs" />
            </Switch>
            <Copyright />
          </Router>
        </SnackbarProvider>
      </Container>
    </React.Fragment>
  );
}
