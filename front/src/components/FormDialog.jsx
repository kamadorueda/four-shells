// Third party libraries
import React from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@material-ui/core';

export const FormDialog = ({
  content,
  isOpen,
  isOpenSet,
  onContinue,
  title,
}) => {
  const dialogOnClose = () => {
    isOpenSet(false);
  };

  return (
    <Dialog open={isOpen} onClose={dialogOnClose}>
      <DialogTitle id='form-dialog-title'>{title}</DialogTitle>
      <DialogContent>
        {content}
      </DialogContent>
      <DialogActions>
        <Button onClick={dialogOnClose} color='secondary'>
          Cancel
        </Button>
        <Button onClick={onContinue} color='primary'>
          Continue
        </Button>
      </DialogActions>
    </Dialog>
  );
}
