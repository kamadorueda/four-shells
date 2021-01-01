// Third party libraries
import React from 'react';
import {
  AppBar,
  Button,
  Link,
  Toolbar,
} from '@material-ui/core';

export const BarNav = () => {
  return (
    <AppBar position='static' color='secondary'>
      <Toolbar variant='dense'>
        <Button size='small'>
          <Link href='/docs#about-nixdb' color='inherit'>
            Why
          </Link>
        </Button>
        <Button size='small'>
          <Link href='/nixdb/search' color='inherit'>
            Search
          </Link>
        </Button>
      </Toolbar>
    </AppBar>
  );
};
