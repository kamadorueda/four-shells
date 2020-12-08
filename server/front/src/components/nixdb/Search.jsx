// Third party
import Levenshtein from 'levenshtein';
import React, { useState } from 'react';
import {
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  Chip,
  Container,
  Grid,
  Link,
  makeStyles,
  TextField,
  Typography,
} from '@material-ui/core';
import {
  SearchOutlined
} from '@material-ui/icons';
import {
  Pagination
} from '@material-ui/lab';

// Local libraries
import { Progress } from '../Progress';
import { useFetchJSON } from './utils';
import { THEME } from '../../utils/theme';

// Constants
const DEFAULT_PKG = 'nix';
const RESULTS_PER_PAGE = 12;

const levenshtein = (a, b) => new Levenshtein(a, b).distance;

const searchString = (item, list) => {
  // Use a mix of Levenshtein distance + grep to offer human-expectable results
  const itemLower = item.toLowerCase();

  const distances = list.map((elem) => {
    const elemLower = elem.toLowerCase();

    let distance;

    if (elemLower === itemLower) {
      distance = 0;
    } else if (elemLower.includes(itemLower)) {
      distance = 1;
    } else {
      distance = levenshtein(itemLower, elemLower);
    }

    return [distance, elem];
  });

  return distances
    // Sort by Levenshtein distance
    .sort((a, b) => a[0] - b[0])
    // Extract the original item
    .map((x) => x[1]);
}

const useStyles = makeStyles((theme) => ({
  card: {
    flex: 1,
  },
  pagination: {
    flex: 1,
  },
}));

const Pkg = ({ pkg }) => {
  const classes = useStyles();
  const dataSource = `/data/pkgs/${pkg}.json`;
  const dataJSON = useFetchJSON(dataSource, {});
  const data =  Object.entries(dataJSON).reverse();

  if (data.length === 0) {
    return <Progress />
  }

  const lastData = data[0][1];
  const description = lastData.meta.description
    ? lastData.meta.description
    : lastData.meta.longDescription
      ? lastData.meta.longDescription
      : '';

  return (
    <Card className={classes.card} variant='outlined'>
      <CardContent>
        <Typography gutterBottom>
          <Link
            href={`/nixdb/pkg/${encodeURIComponent(pkg)}`}
            style={{ color: THEME.own.link }}
          >
            <b>{pkg}</b>
            {pkg === lastData.meta.name
              ? undefined
              : <React.Fragment><br />{lastData.meta.name}</React.Fragment>}
          </Link>
        </Typography>
        {description ? (
          <Typography color='textSecondary' gutterBottom variant='body2'>
            {description}
          </Typography>
        ) : undefined}
      </CardContent>
      <CardActions>
        <Chip
          label={`${data.length} version${data.length >= 2 ? "s" : ""} available`}
          size='small'
          variant='outlined'
        />
      </CardActions>
    </Card>
  )
};

export const Search = ({ pkgs, revs }) => {
  if (pkgs.length === 0 || revs.length === 0) {
    return <Progress />
  }

  const classes = useStyles();

  const [page, setPage] = useState(1);
  const [matchingPkgs, setMatchingPkgs] = useState(
    searchString(DEFAULT_PKG, pkgs),
  );

  const pages = Math.round(matchingPkgs.length / RESULTS_PER_PAGE, 0);
  const endPage = Math.min((page - 0) * RESULTS_PER_PAGE + 0, matchingPkgs.length);
  const startPage = Math.min((page - 1) * RESULTS_PER_PAGE + 1, matchingPkgs.length);

  let deferTimer = setTimeout(() => {}, 100)

  const pageOnChange = (_, newValue) => {
    setPage(newValue);
  };
  const pkgOnChange = (event) => {
    clearTimeout(deferTimer)
    deferTimer = setTimeout(() => {
      setPage(1);
      setMatchingPkgs(searchString(event.target.value, pkgs));
    }, 300)
  };

  return (
    <React.StrictMode>
      <Container maxWidth='md'>
        <Grid container spacing={1} alignItems='flex-end'>
          <Grid item>
            <SearchOutlined />
          </Grid>
          <Grid item>
            <TextField
              label='Package'
              onChange={pkgOnChange}
              defaultValue={DEFAULT_PKG}
            />
          </Grid>
        </Grid>
        <br />
        <Grid container>
          <Pagination
            color='secondary'
            className={classes.pagination}
            count={pages}
            page={page}
            onChange={pageOnChange}
          />
        </Grid>
        <br />
        <Grid
          alignItems='stretch'
          container
          spacing={2}
        >
          {matchingPkgs
            .slice(startPage - 1, endPage)
            .map((pkg) => (
              <Grid item key={pkg} xs={12} sm={6} md={4} lg={4} xl={3}>
                <Pkg key={pkg} pkg={pkg} />
              </Grid>
            ))}
        </Grid>
      </Container>
    </React.StrictMode>
  );
}
