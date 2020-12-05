// Third party
import React from 'react';
import {
  AppBar,
  Button,
  Link,
  Toolbar,
} from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
}));

export const BarBreadcrumb = () => {
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
        <Button color='inherit' size="small">
          <Link color="primary" href="/">Home</Link>
        </Button>
        {components
          .map((_, index) => `/${components.slice(0, index + 1).join('/')}`)
          .map((to) => (
            <React.Fragment>
              /
              <Button color='inherit' key={to} size="small">
                <Link color="primary" href={to}>
                  {componentsMap[to] === undefined
                    ? components[index].slice(0, 7)
                    : componentsMap[to]}
                </Link>
              </Button>
            </React.Fragment>
          ))}
      </Toolbar>
    </AppBar>
  );
};
