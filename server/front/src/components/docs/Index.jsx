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
import {
  makeStyles,
} from '@material-ui/core/styles';

// Local libraries
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { renderMarkdown } from '../Markdown';
import Home from './Home.md';
import Source from './Source.md';

const useStyles = makeStyles((theme) => ({
}));

export const Index = ({ bigScreen }) => {
  const classes = useStyles();
  const pages = [
    { content: Source, path: '/source' },
    { content: Home, path: '/' },
  ];

  return (
    <React.Fragment>
      <BarMain
        bigScreen={bigScreen}
        docs
        home
        source
        sponsors
        title='Four Shells'
        titleLink='/'
      />
      <Container maxWidth='lg'>
        <SnackbarProvider maxSnack={3}>
          <Router basename='/docs'>
            <br />
            <Switch>
              {pages.map(({ content, path }) => (
                <Route
                  key={path}
                  path={path}
                  component={renderMarkdown(content)}
                />
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
