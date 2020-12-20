// Third party
import { SnackbarProvider } from 'notistack';
import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from 'react-router-dom';
import {
  Container,
} from '@material-ui/core';

// Local libraries
import { hasActiveSession } from '../../utils/api';
import { BarBreadcrumb } from '../BarBreadcrumb';
import { BarMain } from '../BarMain';
import { Dashboard } from './Dashboard';
import { Home } from './Home';
import { Copyright } from '../Copyright';

const formatEmail = (email) => {
  const username = email.split('@').slice(0, 1).join('');

  return `${username[0].toUpperCase()}${username.slice(1).toLowerCase()}`;
};

export const Index = ({ bigScreen }) => (
  <React.Fragment>
    <BarMain
      bigScreen={bigScreen}
      docs
      home
      source
      sponsors
      title={hasActiveSession() ? `${formatEmail(globals.session.email)}'s CachIPFS` : 'CachIPFS'}
      titleLink={hasActiveSession() ? '/cachipfs/dashboard' : '/cachipfs'}
    />
    <BarBreadcrumb />
    <Container maxWidth='lg'>
      <SnackbarProvider maxSnack={3}>
        <Router basename='/cachipfs'>
          <br />
          <Switch>
            <Route path='/dashboard' component={Dashboard} />
            <Route path='/' component={Home} />
            <Redirect to='/' />
          </Switch>
          <Copyright />
        </Router>
      </SnackbarProvider>
    </Container>
  </React.Fragment>
);
