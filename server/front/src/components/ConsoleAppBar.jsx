// Third party
import React from 'react';

import {
  AppBar,
  Box,
  Breadcrumbs,
  Link,
  Paper,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  navigation: {
    flexGrow: 1,
    padding: theme.spacing(0.5),
  },
  title: {
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
    <Paper>
      <Box className={classes.navigation}>
        <Breadcrumbs itemsAfterCollapse={2} itemsBeforeCollapse={0} maxItems={3}>
          <Link color="inherit" href="/">
            Home
          </Link>
          {components.map((_, index) => {
            const to = `/${components.slice(0, index + 1).join('/')}`;

            return <Link color="inherit" href={to}>
              {componentsMap[to] === undefined
                ? components[index].slice(0, 7)
                : componentsMap[to]}
            </Link>;
          })}
        </Breadcrumbs>
      </Box>
    </Paper>
  );
};

export const ConsoleAppBar = () => {
  const classes = useStyles();
  const { email } = window.state;

  return (
    <React.StrictMode>
      <AppBar position="relative">
        <Toolbar>
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            className={classes.title}
          >
            {email}
          </Typography>
        </Toolbar>
      </AppBar>
      <NavigationContext />
    </React.StrictMode>
  );
};
