// Third party
import React, { useState } from 'react';
import {
  Button,
  ButtonGroup,
  Chip,
  Container,
  DialogContentText,
  Link,
  TextField,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

// Local libraries
import { useGet, usePost } from '../../api';
import { FormDialog } from '../FormDialog';

const useStyles = makeStyles((theme) => ({
  centered: {
    alignItems: 'center',
    display: 'flex',
    flexDirection: 'column',
    margin: theme.spacing(1),
  },
  chip: {
    margin: theme.spacing(0.5),
  },
  chipList: {
    display: 'flex',
    justifyContent: 'center',
    flexWrap: 'wrap',
    listStyle: 'none',
    padding: theme.spacing(0.5),
    margin: 0,
  },
}));

export const Index = () => {
  const classes = useStyles();

  const [namespaceCreateIsOpen, setNamespaceCreateIsOpen] = useState(false);
  const [namespaceCreateName, setNamespaceCreateName] = useState("");

  // API
  const {
    data: namespacesGetData,
    call: namespacesGet,
  } = useGet('/api/v1/cachipfs/namespaces', []);
  const {
    call: namespacePost,
  } = usePost('/api/v1/cachipfs/namespace/{name}');

  // Handlers
  const namespaceOnCreate = () => {
    setNamespaceCreateIsOpen(false);
    namespacePost({ name: namespaceCreateName });
    namespacesGet();
    setNamespaceCreateName("");
  };
  const namespaceCreateOnChangeName = (event) => {
    setNamespaceCreateName(event.target.value);
  };
  const namespaceCreateOnClick = () => {
    setNamespaceCreateIsOpen(true);
  };

  return (
    <React.StrictMode>
      <Container maxWidth="sm">
        <Typography component="h2" variant="h5" align="center" color="textPrimary">
          Binary Caches
        </Typography>
        <Typography color="textSecondary">
          <br />
          A Binary Cache can store Nixpkgs, Nix builds,
          and in a more general sense /nix/store paths.
          <br />
          <br />
          Results in the binary cache can be used by other machines to avoid
          building from source. Helping you save time, resources,
          and bandwidth.
          <br />
          <br />
        </Typography>
        <Typography component="h2" variant="h6" align="center" color="textPrimary">
          Your Binary Caches
        </Typography>
        <ul className={classes.chipList}>
          {namespacesGetData.map(({ id, name }) => (
            <li key={id}>
              <Link href={`/console/cachipfs/namespace/${encodeURIComponent(id)}`}>
                <Chip className={classes.chip} color="primary" label={name} variant="outlined" />
              </Link>
            </li>
          ))}
        </ul>
      </Container>
      <div className={classes.centered}>
        <ButtonGroup color="primary">
          <Button color="primary" onClick={namespaceCreateOnClick} variant="contained">
            Create
          </Button>
        </ButtonGroup>
      </div>
      <FormDialog
        content={
          <React.Fragment>
            <DialogContentText>Name</DialogContentText>
            <TextField
              autoFocus
              fullWidth
              onChange={namespaceCreateOnChangeName}
              margin="dense"
              value={namespaceCreateName}
            />
          </React.Fragment>
        }
        isOpen={namespaceCreateIsOpen}
        isOpenSet={setNamespaceCreateIsOpen}
        onContinue={namespaceOnCreate}
        title='Create a new Binary Cache'
      />
      <br />
    </React.StrictMode>
  );
};
