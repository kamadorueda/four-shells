// Third party libraries
import React from 'react';
import {
  Divider,
  Link,
  Typography,
} from '@material-ui/core';

// Local libraries
import { URLS } from '../utils/constants';

export const Copyright = () => {
  const currentYear = new Date().getFullYear();

  return (
    <React.Fragment>
      <br />
      <Divider />
      <br />
      <Typography variant="body2" color="textSecondary" align="center">
        Please help us improve by <Link href={URLS.issues}>reporting issues</Link> &hearts;
        <br />
        <br />
        Copyright © <Link color="inherit" href="/">Four Shells</Link> {currentYear}.
      </Typography>
      <br />
    </React.Fragment>
  );
};
