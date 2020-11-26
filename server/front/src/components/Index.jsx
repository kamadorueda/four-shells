// Third party libraries
import React from 'react';
import {
  AppBar,
  Button,
  Container,
  CssBaseline,
  Grid,
  Link,
  Toolbar,
  Typography,
} from '@material-ui/core';

// Local libraries
import { useStyles } from '../styles';

export const Index = () => {
  const classes = useStyles();
  const currentYear = new Date().getFullYear();

  const doLogin = () => {
    window.location.assign('/oauth/google/init')
  };

  return (
    <React.StrictMode>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
          <Typography variant="h6" color="inherit" noWrap>
            Four Shells /&gt;
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

      <Typography variant="body2" color="textSecondary" align="center">
        Copyright © <Link color="inherit" href="/">Four Shells</Link> {currentYear}.
      </Typography>
    </React.StrictMode>
  );
}
