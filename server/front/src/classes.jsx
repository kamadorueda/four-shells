import { makeStyles } from '@material-ui/core/styles';

export const useStylesIndex = makeStyles((theme) => ({
  bodyContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  indexLoginButtons: {
    marginTop: theme.spacing(4),
  },
}));

export const useStylesConsole = makeStyles((theme) => ({
  bodyContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
}));
