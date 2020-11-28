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
  centered: {
    alignItems: 'center',
    display: 'flex',
    flexDirection: 'column',
    margin: theme.spacing(1),
  },
  root: {
    flexGrow: 1,
  },
  paper: {
    color: theme.palette.text.secondary,
    padding: theme.spacing(2),
    textAlign: 'center',
  },
  title: {
    flexGrow: 1,
  },
}));
