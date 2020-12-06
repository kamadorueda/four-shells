// Third party
import React from 'react';
import {
  Button,
  Container,
  Link,
  Typography,
} from '@material-ui/core';

export const Search = ({ pkgs, revs }) => (
  <React.StrictMode>
    <Container maxWidth="md">
      {pkgs.length}
    </Container>
  </React.StrictMode>
);
