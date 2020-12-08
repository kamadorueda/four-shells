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
import Cachipfs from './Cachipfs.md';
import Home from './Home.md';
import Source from './Source.md';
import Sponsors from './Sponsors.md';

const useStyles = makeStyles((theme) => ({
}));

export const Index = ({ bigScreen }) => {
  const classes = useStyles();
  const pages = [
    { content: Cachipfs, path: '/cachipfs' },
    { content: Source, path: '/source' },
    { content: Sponsors, path: '/sponsors' },
    { content: Home, path: '/' },
  ];

  return (
    <React.Fragment>
      <BarMain
        products
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
