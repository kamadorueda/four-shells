// Third party libraries
import React, { useState } from 'react';
import {
  AppBar,
  Container,
  Drawer,
  IconButton,
  Link,
  List,
  ListItem,
  ListItemText,
  makeStyles,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { CodeOutlined, MenuOutlined } from '@material-ui/icons';

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
  about,
  bigScreen,
  contributing,
  contributors,
  docs,
  home,
  sponsors,
  title,
  titleLink,
}) => {
  const classes = useStyles();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const drawerOnOpen = () => {
    setDrawerOpen(true);
  };

  const drawerOnClose = (event) => {
    if (event.type === 'keydown' && ['Shift', 'Tab'].includes(event.key)) {
      return;
    }

    setDrawerOpen(false);
  };

  const items =(
    <List
      className={bigScreen ? classes.navDisplayFlex : undefined}
      component='nav'
    >
      {about ? (
        <Link href='/docs#about-us' color='inherit'>
          <ListItem button>
            <ListItemText primary='About' color='textSecondary' />
          </ListItem>
        </Link>
      ) : undefined}
      {contributing ? (
        <Link href='/docs#contributing' color='inherit'>
          <ListItem button>
            <ListItemText primary='Contributing' color='textSecondary' />
          </ListItem>
        </Link>
      ) : undefined}
      {contributors ? (
        <Link href='/docs#contributors' color='inherit'>
          <ListItem button>
            <ListItemText primary='Contributors' color='textSecondary' />
          </ListItem>
        </Link>
      ) : undefined}
      {docs ? (
        <Link href='/docs' color='inherit'>
          <ListItem button>
            <ListItemText primary='Docs' color='textSecondary' />
          </ListItem>
        </Link>
      ) : undefined}
      {home ? (
        <Link href='/' color='inherit'>
          <ListItem button>
            <ListItemText primary='Home' color='textSecondary' />
          </ListItem>
        </Link>
      ) : undefined}
      {sponsors ? (
        <Link href='/docs#sponsors' color='inherit'>
          <ListItem button>
            <ListItemText primary='Sponsors' color='textSecondary' />
          </ListItem>
        </Link>
      ) : undefined}
    </List>
  );

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

          {bigScreen ? items : (
            <React.Fragment>
              <List className={classes.navDisplayFlex} component='nav'>
                <ListItem button>
                  <IconButton
                    onClick={drawerOnOpen}
                    size='small'
                    style={{ color: 'white' }}
                  >
                    <MenuOutlined />
                  </IconButton>
                </ListItem>
              </List>
              <Drawer anchor='right' open={drawerOpen} onClose={drawerOnClose}>
                {items}
              </Drawer>
            </React.Fragment>
          )}
        </Container>
      </Toolbar>
    </AppBar>
  );
};
