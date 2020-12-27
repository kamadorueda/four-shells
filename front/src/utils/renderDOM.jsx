// Third party libraries
import {
  CssBaseline,
  ThemeProvider,
  useMediaQuery,
} from '@material-ui/core';
import React from 'react';
import ReactDOM from 'react-dom';

// Local libraries
import { THEME } from './theme';

const Child = ({ generator }) => {
  const bigScreen = useMediaQuery((theme) => theme.breakpoints.up('md'));

  return generator({ bigScreen });
};

const Root = ({
  generator,
  title,
}) => {
  window.document.getElementById('title').innerText = title;

  return (
    <React.StrictMode>
      <CssBaseline />
      <ThemeProvider theme={THEME}>
        <Child generator={generator} />
      </ThemeProvider>
    </React.StrictMode>
  );
};

export const render = ({
  generator,
  title,
}) => {
  ReactDOM.render(
    React.createElement(Root, {
      generator,
      title,
    }),
    document.getElementById('root'),
  );
};
