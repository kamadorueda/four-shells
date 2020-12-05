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
import Sponsors from './Sponsors.md';

const useStyles = makeStyles((theme) => ({
}));

export const Index = ({ bigScreen }) => {
  const classes = useStyles();
  const pages = [
    {
      content: Cachipfs,
      path: '/cachipfs',
      title: 'Welcome to CachIPFS documentation!',
    },
    {
      content: Sponsors,
      path: '/sponsors',
      title: 'A small thank you',
    },
    {
      content: Home,
      path: '/',
      title: 'Welcome to Four Shells documentation',
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
              {pages.map(({ content, path, title }) => (
                <Route
                  path={path}
                  component={renderMarkdown({ content, title })}
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
