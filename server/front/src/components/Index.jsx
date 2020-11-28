// Third party libraries
import React from 'react';
import {
  AppBar,
  Button,
  Container,
  CssBaseline,
  Grid,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

// Local libraries
import { Copyright } from './Copyright';

export const useStyles = makeStyles((theme) => ({
  bodyContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  indexLoginButtons: {
    marginTop: theme.spacing(4),
  },
}));

export const Index = () => {
  const classes = useStyles();

  const doLogin = () => {
    window.location.assign('/oauth/google/start')
  };

  return (
    <React.StrictMode>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
          <Typography component="h1" variant="h6" color="inherit" noWrap>
            Four Shells
          </Typography>
        </Toolbar>
      </AppBar>

      <main>
        <div className={classes.bodyContent}>
          <Container maxWidth="sm">
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
                <Grid item>
                  <Button color="primary" onClick={doLogin} variant="outlined" >
                    Get started
                  </Button>
                </Grid>
              </Grid>
            </div>
          </Container>
        </div>
      </main>
      <Copyright />
    </React.StrictMode>
  );
}
