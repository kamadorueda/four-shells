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
import { BarMain } from '../BarMain';
import { BarNav } from '../BarNav';
import { Copyright } from '../Copyright';
import { Markdown } from '../Markdown';
import Home from './Home.md';

const useStyles = makeStyles((theme) => ({
}));

export const Index = ({ bigScreen }) => {
  const classes = useStyles();

  return (
    <React.Fragment>
      <BarMain>
        <b>Four Shells</b>, work in progress!
      </BarMain>
      <BarNav products sponsors source login />
      <Container maxWidth="lg">
        <SnackbarProvider maxSnack={3}>
          <Router basename="/docs">
            <br />
            <Switch>
              <Route path="/">
                <Markdown content={Home} />
              </Route>
              <Redirect to="/" />
            </Switch>
            <Copyright />
          </Router>
        </SnackbarProvider>
      </Container>
    </React.Fragment>
  );
}
