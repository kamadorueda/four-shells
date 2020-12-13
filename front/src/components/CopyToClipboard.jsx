// Third party libraries
import { useSnackbar } from 'notistack';
import React from 'react';
import { CopyToClipboard as ReactCopyToClipboard } from 'react-copy-to-clipboard';

export const CopyToClipboard = ({ children, content }) => {
  const { enqueueSnackbar } = useSnackbar();

  const onCopy = () => {
    enqueueSnackbar('Copied to clipboard', { variant: 'success'});
  };

  return (
    <ReactCopyToClipboard text={content} onCopy={onCopy}>
      {children}
    </ReactCopyToClipboard>
  );
}
