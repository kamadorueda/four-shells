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
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { Markdown } from '../Markdown';
import Home from './Home.md';

export const Index = ({ bigScreen }) => {
  const pages = [
    { content: Home, path: '/', title: 'Four Shells Documentation'},
  ];

  return (
    <React.Fragment>
      <BarMain
        about
        bigScreen={bigScreen}
        contributing
        contributors
        home
        sponsors
        title='Four Shells'
        titleLink='/'
      />
      <Container maxWidth='lg'>
        <SnackbarProvider maxSnack={3}>
          <Router basename='/docs'>
            <br />
            <Switch>
              {pages.map(({ content, path, title }) => (
                <Route
                  key={path}
                  path={path}
                >
                  <Markdown
                    content={content}
                    title={title}
                  />
                </Route>
              ))}
              <Redirect to='/' />
            </Switch>
            <Copyright />
          </Router>
        </SnackbarProvider>
      </Container>
    </React.Fragment>
  );
}
