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
  AppBar,
  Container,
  Toolbar,
} from '@material-ui/core';

// Local libraries
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { renderMarkdown } from '../Markdown';
import { Home } from './Home';
import About from './About.md';
import Contributing from './Contributing.md';
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
            <Route path="/about" component={renderMarkdown({ content: About, title: "About NixDB" })}/>
            <Route path="/contributing" component={renderMarkdown({ content: Contributing, title: "Contributing to NixDB" })}/>
            <Route path="/" component={Home} />
            <Redirect to="/" />
          </Switch>
          <Copyright />
        </Router>
      </SnackbarProvider>
    </Container>
  </React.Fragment>
);
