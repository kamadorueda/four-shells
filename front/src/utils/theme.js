import {
  cyan,
  grey,
  lightBlue,
} from '@material-ui/core/colors';
import {
  createMuiTheme,
} from '@material-ui/core/styles';

// https://material.io/resources/color
export const THEME = createMuiTheme({
  palette: {
    primary: {
      main: grey[900],
    },
    secondary: {
      main: cyan[100],
    },
  },
  own: {
    link: lightBlue[600],
  },
});
