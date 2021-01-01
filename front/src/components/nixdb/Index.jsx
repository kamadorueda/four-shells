// Third party
import { SnackbarProvider } from 'notistack';
import React, { useEffect, useState } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from 'react-router-dom';
import {
  Container, Link, Typography,
} from '@material-ui/core';

// Local libraries
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { Search } from './Search';
import { useFetchJSON } from './utils';
import { BarNav } from './BarNav';
import { Pkg } from './Pkg';
import { setMetadata } from '../../utils/seo';

export const Index = ({ bigScreen }) => {
  setMetadata({
    title: 'NixDB, the Nix packages database',
  });

  const pkgs = useFetchJSON(`/pkgs.json`, []);
  const revs = useFetchJSON(`/revs.json`, []);

  return (
    <React.Fragment>
      <BarMain
        about
        bigScreen={bigScreen}
        contributing
        contributors
        docs
        home
        sponsors
        title='NixDB'
        titleLink='/nixdb'
      />
      <BarNav />
      <Container maxWidth='lg'>
        <SnackbarProvider maxSnack={3}>
          <Router basename='/nixdb'>
            <br />
            <Switch>
              <Route path='/pkg/:pkg/:version' component={Pkg}/>
              <Route path='/pkg/:pkg' component={Pkg}/>
              <Route path='/search'>
                <Search pkgs={pkgs} revs={revs} />
              </Route>
              <Redirect to='/search' />
            </Switch>
          </Router>
        </SnackbarProvider>
      </Container>
      <br />
      <br />
      {pkgs.length > 0 && revs.length > 0 ? (
        <Typography variant='body2' color='textSecondary' align='center'>
          A total of {pkgs.length} packages and {revs.length} commits put in your hands! <br />
        </Typography>
      ) : undefined}
      <Copyright />
    </React.Fragment>
  );
};
