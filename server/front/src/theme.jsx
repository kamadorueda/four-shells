import {
  common,
  grey,
  yellow,
} from '@material-ui/core/colors';
import {
  createMuiTheme,
} from '@material-ui/core/styles';

// https://material.io/resources/color
export const THEME = createMuiTheme({
  palette: {
    primary: {
      contrastText: common['white'],
      dark: grey['A100'],
      light: grey[800],
      main: grey[900],
    },
    secondary: {
      contrastText: common['black'],
      dark: yellow[200],
      light: yellow[50],
      main: yellow[100],
    },
  },
});
