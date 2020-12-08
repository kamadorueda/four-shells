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

export const Home = () => (
  <React.StrictMode>
    <Container maxWidth="md">
      <br />
      <br />
      <Typography component="h1" variant="h3" align="center" color="textPrimary" gutterBottom>
        Build once, retrieve from cache thereafter!
      </Typography>
      <Typography variant="h5" align="center" color="textSecondary" paragraph>
        CachIPFS helps you save time and money by sharing the results of your
        Nix builds.
        <br />
        <br />
        <Button color="secondary" variant="contained">
          {hasActiveSession() ? (
            <Link href={'/cachipfs/dashboard'}>
              Dashboard
            </Link>
          ) : (
            <Link href={getLoginURL('/cachipfs/dashboard')}>
              Login
            </Link>
          )}
        </Button>
        &nbsp;
        <Button color="primary" variant="outlined">
          <Link href='/docs/cachipfs'>
            Read the docs
          </Link>
        </Button>
      </Typography>
    </Container>
  </React.StrictMode>
);
