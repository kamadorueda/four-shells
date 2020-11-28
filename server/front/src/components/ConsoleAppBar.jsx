// Third party
import React from 'react';
import { useLocation } from 'react-router-dom';

import {
  AppBar,
  Badge,
  Box,
  Breadcrumbs,
  Button,
  Container,
  CssBaseline,
  Divider,
  Drawer,
  Grid,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Paper,
  Select,
  Tab,
  TabPanel,
  Tabs,
  Toolbar,
  Typography,
} from '@material-ui/core';
import {
  PowerSettingsNew,
} from '@material-ui/icons';

// Local libraries
import { useStylesConsole } from '../classes';

const COMPONENTS_MAPPING = {
  cachipfs: "CachIPFS",
};

const computeTitle = (path) => (
  path
    .split('/')
    .filter((component) => component)
    .map((component) => COMPONENTS_MAPPING[component] || component)
    .join(' › ')
);

export const ConsoleAppBar = () => {
  const classes = useStylesConsole();
  const location = useLocation();

  const doLogout = () => {
    window.location.assign('/')
  };

  return (
    <React.StrictMode>
      <AppBar position="relative">
        <Toolbar>
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            className={classes.title}
          >
            {computeTitle(location.pathname)}
          </Typography>
          <IconButton color="inherit" onClick={doLogout}>
            <PowerSettingsNew />
          </IconButton>
        </Toolbar>
      </AppBar>
    </React.StrictMode>
  );
};
