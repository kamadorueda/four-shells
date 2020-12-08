// Third party libraries
import React from 'react';
import {
  AppBar,
  Box,
  Container,
  IconButton,
  Link,
  List,
  ListItem,
  ListItemText,
  makeStyles,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { CodeOutlined } from '@material-ui/icons';

const useStyles = makeStyles((theme) => ({
  navbarDisplayFlex: {
    display: 'flex',
    justifyContent: 'space-between'
  },
  navDisplayFlex: {
    display: 'flex',
    justifyContent: 'space-between'
  },
}));

export const BarMain = ({
  products,
  source,
  sponsors,
  title,
  titleLink,
}) => {
  const classes = useStyles();

  return (
    <AppBar position='sticky' color='primary'>
      <Toolbar>
        <Container className={classes.navbarDisplayFlex} maxWidth='lg'>
          <IconButton edge='start' color='inherit'>
            <CodeOutlined />
            &nbsp;
            <Link href={titleLink} color='inherit'>
              <Typography component='h1' variant='h6'>
                {title}
              </Typography>
            </Link>
          </IconButton>
          <List className={classes.navDisplayFlex} component='nav'>
            {products ? (
              <Link href='/' color='inherit'>
                <ListItem button>
                  <ListItemText primary='Products' color='textSecondary' />
                </ListItem>
              </Link>
            ) : undefined}
            {source ? (
              <Link href='/docs/source' color='inherit'>
                <ListItem button>
                  <ListItemText primary='Source' color='textSecondary' />
                </ListItem>
              </Link>
            ) : undefined}
            {sponsors ? (
              <Link href='/docs/sponsors' color='inherit'>
                <ListItem button>
                  <ListItemText primary='Sponsors' color='textSecondary' />
                </ListItem>
              </Link>
            ) : undefined}
          </List>
        </Container>
      </Toolbar>
    </AppBar>
  );
};
