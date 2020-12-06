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

// Local libraries
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { renderMarkdown } from '../Markdown';
import About from './About.md';
import Contributing from './Contributing.md';
import { Home } from './Home';
import { Search } from './Search';
import { BarNav } from './BarNav';

export const Index = ({ bigScreen }) => (
  <React.Fragment>
    <BarMain>
      NixDB
    </BarMain>
    <BarNav />
    <Container maxWidth="lg">
      <SnackbarProvider maxSnack={3}>
        <Router basename="/nixdb">
          <br />
          <Switch>
            <Route path="/about" component={renderMarkdown(About)}/>
            <Route path="/contributing" component={renderMarkdown(Contributing)}/>
            <Route path="/search" component={Search} />
            <Route path="/" component={Home} />
            <Redirect to="/" />
          </Switch>
          <Copyright />
        </Router>
      </SnackbarProvider>
    </Container>
  </React.Fragment>
);
