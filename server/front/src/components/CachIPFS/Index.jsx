// Third party
import React, { useState } from 'react';
import {
  Button,
  ButtonGroup,
  Container,
  DialogContentText,
  Grid,
  Link,
  Paper,
  TextField,
  Typography,
} from '@material-ui/core';

// Local libraries
import { useGet, usePost } from '../../api';
import { useStylesConsole } from '../../classes';
import { FormDialog } from '../FormDialog';

export const Index = () => {
  const classes = useStylesConsole();

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
      <br />
      <Typography variant="h5" align="center" color="textSecondary" paragraph>
        Binary Caches
      </Typography>
      <Container maxWidth="sm">
        <Grid container spacing={2}>
          {namespacesGetData.map(({ id, name }) => (
            <Grid item xs>
              <Link href={`/console/cachipfs/namespace/${encodeURIComponent(id)}`}>
                <Paper className={classes.paper}>{name}</Paper>
              </Link>
            </Grid>
          ))}
        </Grid>
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
