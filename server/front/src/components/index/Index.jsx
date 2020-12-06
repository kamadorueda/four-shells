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
  Link,
  Paper,
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
    marginBottom: theme.spacing(4),
  },
  logoPaper: {
    background: theme.palette.primary.main,
  },
  mainCaption: {
    marginBottom: theme.spacing(4),
    marginTop: theme.spacing(4),
  },
  productCard: {
    maxWidth: 300,
  },
  productText: {
    flex: 1,
    textAlign: 'center',
  },
}));

export const ProductCard = ({
  console,
  description,
  docs,
  image,
  title,
}) => {
  const classes = useStyles();
  const onClick = () => {
    window.location.assign(console);
  };

  return (
    <Card className={classes.productCard}>
      <CardActionArea onClick={onClick}>
        <CardContent>
          <Typography className={classes.productText} gutterBottom variant="h5">
            {title}
          </Typography>
        </CardContent>
        <CardMedia
          component="img"
          height="158"
          image={image}
        />
        <CardContent>
          <Typography className={classes.productText} variant="body2" color="textSecondary">
            {description}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          <Link href={console}>
            Get started
          </Link>
        </Button>
        {docs === undefined ? undefined : (
          <Button size="small" color="primary">
            <Link href={docs}>
              Learn More
            </Link>
          </Button>
        )}
      </CardActions>
    </Card>
  );
};

export const Index = ({ bigScreen }) => {
  const classes = useStyles();

  return (
    <React.Fragment>
      <BarMain>
        <b>Four Shells</b>, work in progress!
      </BarMain>
      <BarNav sponsors source />
      <Container maxWidth="md">
        <div className={classes.mainCaption}>
          <Typography component="h1" variant="h3" align="center" color="textPrimary" gutterBottom>
            Software boosts the world
          </Typography>
          <Typography variant="h5" align="center" color="textSecondary" paragraph>
            Consistent tools that improve your workflows,
            while aiming towards decentralization,
            freedom of choice, privacy and open core values.
          </Typography>
        </div>
      </Container>
      <Container maxWidth="lg">
        <Grid container spacing={2} justify="center">
          <Grid item>
            <ProductCard
              description="Database with Nix packages from all versions, all commits and all channels."
              console='/nixdb'
              image={nix_db_300x158}
              title="NixDB"
            />
          </Grid>
          <Grid item>
            <ProductCard
              description="Encrypted Nix binary cache over IPFS."
              console='/cachipfs'
              docs='/docs/cachipfs'
              image={nix_db_300x158}
              title="CachIPFS"
            />
          </Grid>
        </Grid>
      </Container>
      <Copyright />
    </React.Fragment>
  );
}
