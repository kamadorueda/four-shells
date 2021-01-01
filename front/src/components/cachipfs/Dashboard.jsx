// Third party
import React from 'react';
import {
  Container,
} from '@material-ui/core';

// Local libraries
import { ensureActiveSession, useGet, usePost } from '../../utils/api';
import { setMetadata } from '../../utils/seo';

export const Dashboard = () => {
  setMetadata({
    title: 'CachIPFS, the Nix binary Cache on IPFS',
  });

  ensureActiveSession();

  // API
  const {
    data: meGetData,
    call: meGet,
  } = useGet('/api/v1/me', {});

  return (
    <React.StrictMode>
      <Container maxWidth='lg'>
        API token: {meGetData.cachipfs_api_token}
      </Container>
      <br />
    </React.StrictMode>
  );
};
