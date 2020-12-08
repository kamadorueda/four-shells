// Third party libraries
import { Card, CardContent, Grid, Typography } from '@material-ui/core';
import React from 'react';
import { Redirect, useParams } from 'react-router-dom';
import { Code } from '../Code';

// Local libraries
import { Progress } from '../Progress';
import { useFetchJSON } from './utils';

const Definition = ({
  title,
  children,
}) => (
  <CardContent>
    <Typography gutterBottom>
      {title}
    </Typography>
    {children}
  </CardContent>
);

const DefinitionText = ({ content }) => (
  <Typography color='textSecondary' gutterBottom variant='body2'>
    {content}
  </Typography>
);

const formatMaintainers = (maintainers) => {
  let formatted = [];

  if (maintainers === undefined) {
    return formatted;
  }

  for (let maintainer of maintainers) {
    switch (typeof maintainer) {
      case 'string':
        formatted.push(maintainer);
        break;
      case 'object':
        formatted.push(`${maintainer.name} <${maintainer.email}>`);
        break;
      default:
    }
  }

  return formatted.sort();
}

const formatPlatforms = (platforms) => {
  let formatted = [];

  if ([null, undefined].includes(platforms)) {
    return formatted;
  }

  for (let platform of platforms) {
    switch (typeof platform) {
      case "string":
        formatted.push(platform);
        break;
      default:
    }
  }

  return formatted.sort();
}

export const Pkg = () => {
  const { pkg, version } = useParams();

  const dataJSON = useFetchJSON(`/data/pkgs/${pkg}.json`, {});
  const data =  Object.entries(dataJSON).reverse();

  if (data.length === 0) {
    return <Progress />
  }

  if (version === undefined) {
    return <Redirect to={`/pkg/${encodeURIComponent(pkg)}/${encodeURIComponent(data[0][0])}`} />;
  }

  const versionData = dataJSON[version];
  const versionDataLastRev = versionData?.revs[1];
  const versions = data.map(([version, _]) => version);
  const nixpkgs = `https://github.com/NixOS/nixpkgs/archive/${versionDataLastRev}.tar.gz`;
  const nixEnv = `
    # Version: ${version}
    nix-env -i ${pkg} -f ${nixpkgs}
  `;
  const nixShell = `
    # Version: ${version}
    nix-shell -p ${pkg} -I nixpkgs=${nixpkgs}
  `;
  const nixBuild = `
    let
      pkgs = import <nixpkgs> { };

      # Version: ${version}
      ${pkg} = (import (pkgs.fetchzip {
        url = "https://github.com/nixos/nixpkgs/archive/${versionDataLastRev}.zip";
        # Please update this hash with the one nix says on the first build attempt
        sha256 = "0000000000000000000000000000000000000000000000000000000000000000";
      }) { }).${pkg};
    in
      ...
  `;

  const pkgName = (
    versionData?.meta?.name === undefined
    || versionData?.meta?.name === pkg
  ) ? ''
    : `, also known as ${versionData?.meta?.name}`;

  return (
    <Card>
      <Definition title='Package'>
        <DefinitionText content={`${pkg}${pkgName}`} />
      </Definition>
      <Definition title='This package version'>
        <DefinitionText content={version} />
      </Definition>
      <Definition title='All versions'>
        <Grid container>
          {versions.map((v) => (
            <Grid key={v} item xs={6} sm={4} md={3} lg={3} xl={2}>
              <DefinitionText content={v} />
            </Grid>
          ))}
        </Grid>
      </Definition>
      <Definition title='Description'>
        <DefinitionText content={versionData?.meta?.description}/>
      </Definition>
      <Definition title='Long Description'>
        <DefinitionText content={versionData?.meta?.long_description}/>
      </Definition>
      <Definition title='Home Page'>
        <DefinitionText content={versionData?.meta?.homepage}/>
      </Definition>
      <Definition title='License'>
        <DefinitionText content={versionData?.meta?.license?.fullName}/>
      </Definition>
      <Definition title='Maintainers'>
        <Grid container>
          {formatMaintainers(versionData?.meta?.maintainers).map((m) => (
            <Grid key={m} item xs={6} sm={4} md={3} lg={3} xl={2}>
              <DefinitionText content={m} />
            </Grid>
          ))}
        </Grid>
      </Definition>
      <Definition title='Interactive shell'>
        <Code content={nixShell} copyable={true} lang='bash' />
      </Definition>
      <Definition title='Install in your system'>
        <Code content={nixEnv} copyable={true} lang='bash' />
      </Definition>
      <Definition title='Use in an expression'>
        <Code content={nixBuild} copyable={true} lang='nix' />
      </Definition>
      <Definition title='Commits range'>
        <DefinitionText content={
          `${versionData?.revs[0]} -> ${versionData?.revs[1]}`
        } />
      </Definition>
      <Definition title='Raw data'>
        <DefinitionText content={versionData?.meta?.license?.fullName}/>
      </Definition>
      <Definition title='Available platforms'>
        <Grid container>
          {formatPlatforms(versionData?.meta?.platforms).map((p) => (
            <Grid key={p} item xs={6} sm={4} md={3} lg={3} xl={2}>
              <DefinitionText content={p} />
            </Grid>
          ))}
        </Grid>
      </Definition>
    </Card>
  );
}
