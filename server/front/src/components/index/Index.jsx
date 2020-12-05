// Third party libraries
import React from 'react';
import {
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  CardMedia,
  Container,
  Grid,
  Typography,
} from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';

// Local libraries
import { BarMain } from '../BarMain';
import { BarNav } from '../BarNav';
import { Copyright } from '../Copyright';
import nix_db_300x158 from '../../../static/nix_db_300x158.png';

export const useStyles = makeStyles((theme) => ({
  indexLoginButtons: {
    marginTop: theme.spacing(4),
  },
  logoPaper: {
    background: theme.palette.primary.main,
  },
  productCard: {
    maxWidth: 300,
  },
}));

export const ProductCard = ({
  description,
  title,
}) => {
  const classes = useStyles();

  return (
    <Card className={classes.productCard}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="158"
          image={nix_db_300x158}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            {title}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            {description}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          Learn More
        </Button>
      </CardActions>
    </Card>
  );
};

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
      <BarNav docs sponsors source />
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
        <ProductCard
          description="A database with Nix packages from all versions, all commits and all channels."
          title="NixDB"
        />
      </Container>
      <Copyright />
    </React.Fragment>
  );
}
