// Third party
import React from 'react';

import {
  AppBar,
  Box,
  Breadcrumbs,
  Button,
  Link,
  Paper,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  consoleTitle: {
    margin: theme.spacing(2),
  },
  breadcrumb: {
    backgroundColor: theme.palette.secondary.main,
  },
  navigation: {
    flexGrow: 1,
  },
}));

const NavigationContext = () => {
  const classes = useStyles();
  const pathname = window.location.pathname;
  const components = pathname.split('/').filter((component) => component);
  const componentsMap = {
    '/console': 'Console',
    '/console/cachipfs': 'CachIPFS',
    '/console/cachipfs/namespace': 'Namespace',
  };

  return (
    <AppBar position="static" color="secondary">
      <Toolbar variant='dense'>
        <Button color='inherit' size="small"><Link color="primary" href="/">
          Home
        </Link></Button>
        {components.map((_, index) => {
          const to = `/${components.slice(0, index + 1).join('/')}`;

          return (
            <React.Fragment>
              /
              <Button color='inherit' size="small"><Link color="primary" href={to}>
                {componentsMap[to] === undefined
                  ? components[index].slice(0, 7)
                  : componentsMap[to]}
              </Link></Button>
            </React.Fragment>
          );
        })}
      </Toolbar>
    </AppBar>
  );
};

const formatEmail = (email) => {
  const username = email.split('@').slice(0, 1).join('');

  return `${username[0].toUpperCase()}${username.slice(1).toLowerCase()}`;
};

export const ConsoleAppBar = () => {
  const classes = useStyles();
  const { email } = window.state;

  return (
    <React.StrictMode>
      <AppBar position="sticky" color="primary">
        <Toolbar>
          <Typography
            color="inherit"
            component="h1"
            variant="h6"
          >
            {formatEmail(email)}'s Console
          </Typography>
        </Toolbar>
      </AppBar>
      <NavigationContext />
    </React.StrictMode>
  );
};
