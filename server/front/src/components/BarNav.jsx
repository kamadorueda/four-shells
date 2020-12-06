// Third party libraries
import React from 'react';
import {
  AppBar,
  Button,
  Link,
  Toolbar,
} from '@material-ui/core';
import { URLS } from '../utils/constants';

export const BarNav = ({
  products,
  sponsors,
  source,
}) => {
  return (
    <AppBar position="static" color="secondary">
      <Toolbar variant='dense'>
        {products ? (
          <Button size="small"><Link href={URLS.products} color="inherit">
          Products
          </Link></Button>
        ) : undefined}
        {source ? (
          <Button size="small"><Link href={URLS.source} color="inherit">
            Source
          </Link></Button>
        ) : undefined}
        {sponsors ? (
          <Button size="small"><Link href={URLS.sponsors} color="inherit">
            Sponsors
          </Link></Button>
        ) : undefined}
      </Toolbar>
    </AppBar>
  );
};
