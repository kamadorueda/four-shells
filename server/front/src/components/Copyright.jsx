// Third party libraries
import React from 'react';
import {
  Link,
  Typography,
} from '@material-ui/core';

export const Copyright = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Typography variant="body2" color="textSecondary" align="center">
      Copyright © <Link color="inherit" href="/">Four Shells</Link> {currentYear}.
    </Typography>
  );
};
