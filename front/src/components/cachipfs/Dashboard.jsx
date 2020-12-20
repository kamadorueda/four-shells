// Third party
import React from 'react';
import {
  Container,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

// Local libraries
import { ensureActiveSession, useGet, usePost } from '../../utils/api';

const useStyles = makeStyles((theme) => ({
}));

export const Dashboard = () => {
  ensureActiveSession();

  // API
  const {
    data: meGetData,
    call: meGet,
  } = useGet('/api/v1/me', {});

  return (
    <React.StrictMode>
      <Container maxWidth='lg'>
        Work in progress!
      </Container>
      <br />
    </React.StrictMode>
  );
};
