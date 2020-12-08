// Third party
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Avatar,
  Card,
  Container,
  IconButton,
  LinearProgress,
  Typography,
  CardHeader,
  CardActions,
  CardContent,
} from '@material-ui/core';
import {
  CachedOutlined,
  FileCopyOutlined,
  VisibilityOutlined,
  VisibilityOffOutlined,
  VpnKeyOutlined,
} from '@material-ui/icons';
import { makeStyles } from '@material-ui/core/styles';

// Local libraries
import { useGet, usePost } from '../../utils/api';
import { CopyToClipboard } from '../CopyToClipboard';

const useStyles = makeStyles((theme) => ({
  listNested: {
    paddingLeft: theme.spacing(8),
  },
}));

export const Namespace = () => {
  const { id } = useParams();
  const classes = useStyles();
  const [visibleA, setVisibleA] = useState(false);
  const [visibleR, setVisibleR] = useState(false);
  const [visibleW, setVisibleW] = useState(false);

  // API
  const {
    call: namespaceGet,
    data: namespaceGetData,
    loading: namespaceLoading,
  } = useGet('/api/v1/cachipfs/namespace/{id}', {}, { id });
  const {
    call: namespacePost,
  } = usePost('/api/v1/cachipfs/namespace/{id}/rotate/{entity}', {});

  // Handlers
  const rotateAOnClick = () => {
    namespacePost({ id, entity: 'token_admin'});
    setTimeout(namespaceGet, 2000);
  };
  const rotateROnClick = () => {
    namespacePost({ id, entity: 'token_read'});
    setTimeout(namespaceGet, 2000);
  };
  const rotateWOnClick = () => {
    namespacePost({ id, entity: 'token_write'});
    setTimeout(namespaceGet, 2000);
  };
  const visibleAOnClick = () => {
    setVisibleA(!visibleA);
  };
  const visibleROnClick = () => {
    setVisibleR(!visibleR);
  };
  const visibleWOnClick = () => {
    setVisibleW(!visibleW);
  };

  if (namespaceLoading) {
    return <LinearProgress />;
  }

  return (
    <React.Fragment>
      <Container maxWidth='xs'>
        <Typography component='h2' variant='h5' align='center' color='textPrimary'>
          Using <b>{namespaceGetData.name.toUpperCase()}</b> Binary Cache
        </Typography>
        <Typography color='textSecondary'>
          <br />
          In order to configure Nix to use this binary cache you'll need
          to configure your <b>cachipfs</b> client with the following tokens.
          <br />
          <br />
          You can copy or rotate access tokens as needed.
          Once a token is rotated it cannot be restored.
          <br />
          <br />
        </Typography>
        <Card>
          <CardHeader
            avatar={<Avatar><VpnKeyOutlined /></Avatar>}
            title='Read Access Token'
          />
          <CardContent>
            <Typography variant='body2' color='textSecondary' component='p'>
              {visibleR ? namespaceGetData.token_read : '*'.repeat(32)}
            </Typography>
          </CardContent>
          <CardActions disableSpacing>
            <IconButton onClick={visibleROnClick} >
              {visibleR ? <VisibilityOffOutlined /> : <VisibilityOutlined />}
            </IconButton>
            <CopyToClipboard content={namespaceGetData.token_read}>
              <IconButton>
                <FileCopyOutlined />
              </IconButton>
            </CopyToClipboard>
            <IconButton onClick={rotateROnClick}>
              <CachedOutlined />
            </IconButton>
          </CardActions>
        </Card>
        <br />
        <Card>
          <CardHeader
            avatar={<Avatar><VpnKeyOutlined /></Avatar>}
            title='Write Access Token'
          />
          <CardContent>
            <Typography variant='body2' color='textSecondary' component='p'>
              {visibleW ? namespaceGetData.token_write : '*'.repeat(32)}
            </Typography>
          </CardContent>
          <CardActions disableSpacing>
            <IconButton onClick={visibleWOnClick} >
              {visibleW ? <VisibilityOffOutlined /> : <VisibilityOutlined />}
            </IconButton>
            <CopyToClipboard content={namespaceGetData.token_write}>
              <IconButton>
                <FileCopyOutlined />
              </IconButton>
            </CopyToClipboard>
            <IconButton onClick={rotateWOnClick}>
              <CachedOutlined />
            </IconButton>
          </CardActions>
        </Card>
        <br />
        <Card>
          <CardHeader
            avatar={<Avatar><VpnKeyOutlined /></Avatar>}
            title='Admin Access Token'
          />
          <CardContent>
            <Typography variant='body2' color='textSecondary' component='p'>
              {visibleA ? namespaceGetData.token_admin : '*'.repeat(32)}
            </Typography>
          </CardContent>
          <CardActions disableSpacing>
            <IconButton onClick={visibleAOnClick} >
              {visibleA ? <VisibilityOffOutlined /> : <VisibilityOutlined />}
            </IconButton>
            <CopyToClipboard content={namespaceGetData.token_admin}>
              <IconButton>
                <FileCopyOutlined />
              </IconButton>
            </CopyToClipboard>
            <IconButton onClick={rotateAOnClick}>
              <CachedOutlined />
            </IconButton>
          </CardActions>
        </Card>
      </Container>
    </React.Fragment>
  );
};
