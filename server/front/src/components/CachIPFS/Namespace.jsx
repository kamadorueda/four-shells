// Third party
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Button,
  ButtonGroup,
  Container,
  DialogContentText,
  Grid,
  Paper,
  TextField,
  Typography,
} from '@material-ui/core';

// Local libraries
import { useGet, usePost } from '../../api';
import { useStylesConsole } from '../../classes';
import { FormDialog } from '../FormDialog';

export const Namespace = () => {
  const { id } = useParams();

  return (
    <React.Fragment>
      {id}
    </React.Fragment>
  );
};
