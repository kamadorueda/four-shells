// Third party
import React from 'react';
import {
  Button,
  Chip,
  Container,
  Link,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

// Local libraries
import { OnClickDoLogin } from '../../utils/api';

export const Home = () => (
  <React.StrictMode>
    <Container maxWidth="md">
      <div className={classes.mainCaption}>
        <Typography component="h1" variant="h3" align="center" color="textPrimary" gutterBottom>
          Build once, retrieve from cache thereafter!
        </Typography>
        <Typography variant="h5" align="center" color="textSecondary" paragraph>
          CachIPFS helps you save time and money by sharing the results of your
          Nix builds.
        </Typography>
        <Button color="secondary" onClick={OnClickDoLogin('/cachipfs/dashboard')} variant="outlined">
          Login
        </Button>
      </div>
    </Container>
  </React.StrictMode>
);
