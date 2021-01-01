// Third party
import React from 'react';
import {
  Button,
  Container,
  Link,
  Typography,
} from '@material-ui/core';

// Local libraries
import { getLoginURL, hasActiveSession } from '../../utils/api';
import { setMetadata } from '../../utils/seo';

export const Home = () => {
  setMetadata({
    title: 'CachIPFS, the Nix binary Cache on IPFS',
  });

  return (
    <React.StrictMode>
      <Container maxWidth='md'>
        <br />
        <br />
        <Typography component='h1' variant='h3' align='center' color='textPrimary' gutterBottom>
          Build once, retrieve from cache thereafter!
        </Typography>
        <Typography variant='h5' align='center' color='textSecondary' paragraph>
          CachIPFS helps you save time and money by sharing the results of your
          Nix builds.
          <br />
          <br />
          {hasActiveSession() ? (
            <Button color='secondary' variant='contained'>
              <Link href={'/cachipfs/dashboard'}>
                Dashboard
              </Link>
            </Button>
          ) : (
            <React.Fragment>
              <Button color='secondary' variant='contained'>
                <Link href={getLoginURL('/cachipfs/dashboard')}>
                  Login
                </Link>
              </Button>
              &nbsp;
              <Button color='primary' variant='outlined'>
                <Link href={getLoginURL('/cachipfs/dashboard')}>
                  Register
                </Link>
              </Button>
            </React.Fragment>
          )}
          &nbsp;
          <Button color='primary' variant='outlined'>
            <Link href='/docs#about-cachipfs'>
              Read the docs
            </Link>
          </Button>
        </Typography>
      </Container>
    </React.StrictMode>
  );
};
