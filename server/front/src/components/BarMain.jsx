// Third party libraries
import React from 'react';
import {
  AppBar,
  Link,
  Toolbar,
  Typography,
} from '@material-ui/core';

export const BarMain = ({ children }) => {
  return (
    <AppBar position="sticky" color="primary">
      <Toolbar>
        <Typography
          color="inherit"
          component="h1"
          variant="h6"
        >
          <Link href='/' color="inherit">
            {children}
          </Link>
        </Typography>
      </Toolbar>
    </AppBar>
  );
};
