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
  Typography,
} from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';

// Local libraries
import { BarMain } from '../BarMain';
import { Copyright } from '../Copyright';
import { THEME } from '../../utils/theme';
import nix_db_300x158 from '../../../static/nix_db_300x158.png';
import { setMetadata } from '../../utils/seo';

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
          <Typography className={classes.productText} gutterBottom variant='h5'>
            {title}
          </Typography>
        </CardContent>
        <CardMedia
          component='img'
          height='158'
          image={image}
        />
        <CardContent>
          <Typography className={classes.productText} variant='body2' color='textSecondary'>
            {description}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size='small' color='primary'>
          <Link href={console}>
            Get started
          </Link>
        </Button>
        {docs === undefined ? undefined : (
          <Button size='small' color='primary'>
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
  setMetadata({
    title: 'Four Shells, Open Source technologies around Nix and IPFS',
  });

  const classes = useStyles();

  return (
    <React.Fragment>
      <BarMain
        about
        bigScreen={bigScreen}
        contributing
        contributors
        docs
        sponsors
        title='Four Shells'
        titleLink='/'
      />
      <Container maxWidth='md'>
        <div className={classes.mainCaption}>
          <Typography variant='h5' align='center' color='textSecondary' paragraph>
            <Link
              href='https://github.com/kamadorueda/four-shells/blob/main/LICENSE'
              style={{ color: THEME.own.link }}
            >
              Open Source
            </Link>
            &nbsp;technologies around&nbsp;
            <Link href='https://nixos.org' style={{ color: THEME.own.link }}>
              Nix
            </Link>
            &nbsp;and&nbsp;
            <Link href='https://ipfs.io' style={{ color: THEME.own.link }}>
              IPFS
            </Link>
          </Typography>
        </div>
      </Container>
      <Container maxWidth='lg'>
        <Grid container spacing={2} justify='center'>
          <Grid item>
            <ProductCard
              description='Database with Nix packages from all versions, all commits and all channels.'
              console='/nixdb'
              docs='/docs#about-nixdb'
              image={nix_db_300x158}
              title='NixDB'
            />
          </Grid>
          <Grid item>
            <ProductCard
              description='Encrypted Nix binary cache over IPFS. Work in progress!'
              console='/cachipfs'
              docs='/docs#about-cachipfs'
              image={nix_db_300x158}
              title='CachIPFS'
            />
          </Grid>
        </Grid>
      </Container>
      <Copyright />
    </React.Fragment>
  );
}
