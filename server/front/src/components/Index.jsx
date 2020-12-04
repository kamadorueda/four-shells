// Third party libraries
import React from 'react';
import {
  AppBar,
  Button,
  Container,
  Grid,
  Link,
  Paper,
  Toolbar,
  Typography,
} from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';

// Local libraries
import { Copyright } from './Copyright';
import { URLS } from '../utils/constants';

export const useStyles = makeStyles((theme) => ({
  bodyContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  indexLoginButtons: {
    marginTop: theme.spacing(4),
  },
  logoPaper: {
    background: theme.palette.primary.main,
  },
}));

export const Index = ({ bigScreen }) => {
  const classes = useStyles();

  const doLogin = () => {
    window.location.assign('/oauth/google/start')
  };

  return (
    <React.Fragment>
      <AppBar position="sticky" color="primary">
        <Toolbar>
          <Typography
            color="inherit"
            component="h1"
            variant="h6"
          >
            <Link href='/' color="inherit">
              <b>Four Shells</b>, work in progress!
            </Link>
          </Typography>
        </Toolbar>
      </AppBar>
      <AppBar position="static" color="secondary">
        <Toolbar variant='dense'>
          <Button size="small"><Link href={URLS.products} color="inherit">
            Products
          </Link></Button>
          <Button size="small"><Link href={URLS.docs} color="inherit">
            Docs
          </Link></Button>
          <Button size="small"><Link href={URLS.source} color="inherit">
            Source
          </Link></Button>
          <Button size="small"><Link href={URLS.sponsors} color="inherit">
            Sponsors
          </Link></Button>
        </Toolbar>
      </AppBar>
      <main>
        <div className={classes.bodyContent}>
          <Container maxWidth="lg">
            <Typography component="h1" variant="h3" align="center" color="textPrimary" gutterBottom>
              Software enables productivity
            </Typography>
            <Typography variant="h5" align="center" color="textSecondary" paragraph>
              Consistent tools to improve your workflows and power up your systems.
            </Typography>
            <div className={classes.indexLoginButtons}>
              <Grid container spacing={2} justify="center">
                <Grid item>
                  <Button color="primary" onClick={doLogin} variant="contained" >
                    Login to the console
                  </Button>
                </Grid>
              </Grid>
            </div>
          </Container>
        </div>
      </main>
      <Copyright />
    </React.Fragment>
  );
}
