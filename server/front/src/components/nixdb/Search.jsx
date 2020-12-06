// Third party
import Levenshtein from 'levenshtein';
import React, { useState } from 'react';
import {
  Button,
  Container,
  Grid,
  Link,
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

// Constants
const DEFAULT_PKG = 'nix';
const RESULTS_PER_PAGE = 10;

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

const Pkg = ({ pkg }) => {
  const dataSource = `/data/pkgs/${pkg}.json`;
  const dataJSON = useFetchJSON(dataSource, {});
  const data =  Object.entries(dataJSON).reverse();

  if (data.length === 0) {
    return <Progress />
  }

  const lastData = data[0][1];
  const pkgLink = `/pkg/${encodeURIComponent(pkg)}`;

  return (
    <React.Fragment>
      xx
    </React.Fragment>
  )
};

export const Search = ({ pkgs, revs }) => {
  if (pkgs.length === 0 || revs.length === 0) {
    return <Progress />
  }

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
      <Container maxWidth="md">
        <Grid container spacing={1} alignItems="flex-end">
          <Grid item>
            <SearchOutlined />
          </Grid>
          <Grid item>
            <TextField
              label="Package"
              onChange={pkgOnChange}
              defaultValue={DEFAULT_PKG}
            />
          </Grid>
        </Grid>
        <br />
        <Pagination count={pages} page={page} onChange={pageOnChange} />
        <br />
        {matchingPkgs
          .slice(startPage - 1, endPage)
          .map((pkg) => <Pkg pkg={pkg} />)}
      </Container>
    </React.StrictMode>
  );
}
