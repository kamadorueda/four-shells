// Third party
import {
  CssBaseline,
  ThemeProvider,
  useMediaQuery,
} from '@material-ui/core';
import React from 'react';
import ReactDOM from 'react-dom';

// Local
import { Console } from './components/Console';
import { THEME } from './theme';

const Wrapper = () => {
  const bigScreen = useMediaQuery((theme) => theme.breakpoints.up('lg'));

  return <Console bigScreen={bigScreen} />;
};

const Root = () => (
  <React.StrictMode>
    <CssBaseline />
    <ThemeProvider theme={THEME}>
      <Wrapper />
    </ThemeProvider>
  </React.StrictMode>
);

ReactDOM.render(
  React.createElement(Root),
  document.getElementById("root"),
);
