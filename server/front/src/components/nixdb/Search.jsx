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

export const Search = ({ pkgs, revs }) => {
  if (pkgs.length === 0 || revs.length === 0) {
    return <Progress />
  }

  // Pagination
  const [page, setPage] = useState(1);
  const pages = Math.round(pkgs.length / RESULTS_PER_PAGE, 0);
  const pageOnChange = (_, newValue) => {
    setPage(newValue);
  };

  // Selected Package
  const [pkg, setPkg] = useState(DEFAULT_PKG);
  const pkgOnChange = (event) => {
    setPkg(event.target.value);
  };

  // Matching packages
  const [matchingPkgs, setMatchingPkgs] = useState(
    searchString(DEFAULT_PKG, pkgs),
  );
  const [endPage, startPage] = [
    Math.min((page - 0) * RESULTS_PER_PAGE + 0, matchingPkgs.length),
    Math.min((page - 1) * RESULTS_PER_PAGE + 1, matchingPkgs.length),
  ];
  const matchingPkgsOnPage = matchingPkgs.slice(startPage - 1, endPage);

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
              value={pkg}
            />
          </Grid>
        </Grid>
        <br />
        <Pagination count={pages} page={page} onChange={pageOnChange} />
        <br />
        {JSON.stringify(matchingPkgsOnPage)}
      </Container>
    </React.StrictMode>
  );
}
