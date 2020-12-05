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
import { renderMarkdown } from '../Markdown';
import Cachipfs from './Cachipfs.md';
import Home from './Home.md';

const useStyles = makeStyles((theme) => ({
}));

export const Index = ({ bigScreen }) => {
  const classes = useStyles();
  const pages = [
    {
      content: Cachipfs,
      path: '/cachipfs',
      product: 'CachIPFS',
    },
    {
      content: Home,
      path: '/',
      product: 'Four Shells',
    },
  ];

  return (
    <React.Fragment>
      <BarMain>
        <b>Four Shells</b>, work in progress!
      </BarMain>
      <BarNav login products source sponsors/>
      <Container maxWidth="lg">
        <SnackbarProvider maxSnack={3}>
          <Router basename="/docs">
            <br />
            <Switch>
              {pages.map(({ content, path, product }) => (
                <Route
                  path={path}
                  component={renderMarkdown({ content, product })}
                />
              ))}
              <Redirect to="/" />
            </Switch>
            <Copyright />
          </Router>
        </SnackbarProvider>
      </Container>
    </React.Fragment>
  );
}
