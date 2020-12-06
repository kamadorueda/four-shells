// Third party
import { SnackbarProvider } from 'notistack';
import React, { useEffect, useState } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import {
  Container, Link, Typography,
} from '@material-ui/core';

// Local libraries
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { renderMarkdown } from '../Markdown';
import About from './About.md';
import Contributing from './Contributing.md';
import { Search } from './Search';
import { BarNav } from './BarNav';

const DATA_URL = 'https://raw.githubusercontent.com/kamadorueda/nixpkgs-db/latest';

const fetchJSON = async (url) => {
  let response = await fetch(url);

  while (!response.ok || response.status !== 200) {
    response = await fetch(url);
  }

  return await response.json();
};

const useFetchJSON = (url, defaultData) => {
  const [data, setData] = useState(defaultData);

  useEffect(() => {
    (async () => setData(await fetchJSON(url)))();
  }, [url]);

  return data;
}

export const Index = ({ bigScreen }) => {
  const pkgs = useFetchJSON(`${DATA_URL}/data/pkgs.json`, []);
  const revs = useFetchJSON(`${DATA_URL}/data/revs.json`, []);

  return (
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
              <Route path="/search">
                <Search pkgs={pkgs} revs={revs} />
              </Route>
              <Redirect to="/search" />
            </Switch>
          </Router>
        </SnackbarProvider>
      </Container>
      <Typography variant="body2" color="textSecondary" align="center">
        A total of {pkgs.length} packages and {revs.length} commits put in your hands! <br />
      </Typography>
      <Copyright />
    </React.Fragment>
  );
};
