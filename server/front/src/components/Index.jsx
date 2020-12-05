// Third party libraries
import React from 'react';
import {
  Button,
  Container,
  Grid,
  Typography,
} from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';

// Local libraries
import { BarMain } from './BarMain';
import { BarNav } from './BarNav';
import { Copyright } from './Copyright';

export const useStyles = makeStyles((theme) => ({
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
      <BarMain>
        <b>Four Shells</b>, work in progress!
      </BarMain>
      <BarNav docs products sponsors source />
      <Container maxWidth="lg">
        <br />
        <br />
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
      <Copyright />
    </React.Fragment>
  );
}
