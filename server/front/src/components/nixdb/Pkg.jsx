// Third party libraries
import {
  Card,
  CardContent,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  TextField,
  Typography,
} from '@material-ui/core';
import React, { useEffect, useState } from 'react';
import { Redirect, useParams } from 'react-router-dom';
import { Code } from '../Code';

// Local libraries
import { Progress } from '../Progress';
import { useFetchJSON } from './utils';

// Constants
const FORMATS_FUNCTIONS = {
  "AsciiDoc": (imageURL, linkURL) => `
    image:${imageURL}[link="${linkURL}"]
  `,
  "HTML": (imageURL, linkURL) => `
    <a href="${linkURL}">
      <img src="${imageURL}">
    </a>
  `,
  "Markdown": (imageURL, linkURL) => `
    [![](${imageURL})](${linkURL})
  `,
  "ReStructuredText": (imageURL, linkURL) => `
    .. image:: ${imageURL}
      :target: ${linkURL}
  `,
};
const FORMATS = Object.keys(FORMATS_FUNCTIONS);
export const COLORS = [
  "blue",
  "blueviolet",
  "brightgreen",
  "green",
  "lightgrey",
  "orange",
  "red",
  "yellow",
  "yellowgreen",
];

export const STYLES = [
  "flat",
  "flat-square",
  "plastic",
  "for-the-badge",
];

export const badge = ({
  color = "green",
  label,
  labelColor = "grey",
  logo = "NixOS",
  logoColor = "white",
  pkg,
  style = "flat",
}) => {
  const url = new URL("https://img.shields.io/endpoint");

  url.searchParams.set("color", color);
  url.searchParams.set("label", label === undefined ? pkg : label);
  url.searchParams.set("labelColor", labelColor);
  url.searchParams.set("logo", logo);
  url.searchParams.set("logoColor", logoColor);
  url.searchParams.set("style", style);
  url.searchParams.set("url", `https://raw.githubusercontent.com/kamadorueda/nixpkgs-db/latest/data/badges/${pkg}.json`);

  return url.toString();
}

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

const Badge = ({ pkg }) => {
  const [badgeId, setBadgeId] = useState('flat/blue');
  const [badgesData, setBadgesData] = useState([]);
  const [content, setContent] = useState("");
  const [format, setFormat] = useState(FORMATS[2]);
  const [label, setLabel] = useState(pkg);

  const linkURL = `https://4shells.com/nixdb/pkg/${encodeURIComponent(pkg)}`;

  useEffect(() => {
    const newBadgesData = [].concat.apply([],
      STYLES.map((style) => COLORS.map((color) => {
        const imageURL = badge({ color, label, pkg, style });
        const badgeContent = FORMATS_FUNCTIONS[format](imageURL, linkURL);

        return {
          badgeContent,
          color,
          imageURL,
          style,
        };
      }))
    );

    setBadgesData(newBadgesData);
    setContent(newBadgesData[0].badgeContent);
  }, [format, label, linkURL, pkg])

  const onBadgeSelection = (content) => (event) => {
    setContent(content);
    setBadgeId(event.target.value);
  };
  const onChangeFormat = (event) => {
    setFormat(event.target.value);
  };
  const onChangeLabel = (event) => {
    setLabel(event.target.value);
  };

  return (
    <React.Fragment>
      <DefinitionText content='Add the badge of your preference to your project!'/>
      <DefinitionText content='It will tell your users the number of releases they can install with Nix and link to this page so they can get more information!'/>
      <br />
      <FormControl variant="outlined">
        <InputLabel>Format</InputLabel>
        <Select
          value={format}
          onChange={onChangeFormat}
          label="Format"
        >
          {FORMATS.map((f) => <MenuItem key={f} value={f}>{f}</MenuItem>)}
        </Select>
        <br />
        <TextField
          defaultValue={pkg}
          label="Custom label"
          onChange={onChangeLabel}
          value={label}
          variant='outlined'
        />
      </FormControl>
      <br />
      <br />
      <Grid container>
        <RadioGroup row>
          {badgesData.map(({ badgeContent, color, imageURL, style }) => {
            const radioID = `${style}/${color}`;

            return (
              <Grid item xs={12} sm={6} md={4}>
                <Radio
                  checked={radioID == badgeId}
                  onChange={onBadgeSelection(badgeContent)}
                  size='small'
                  value={radioID}
                />
                <img alt={radioID} src={imageURL}/>
              </Grid>
            );
          })}
        </RadioGroup>
      </Grid>
      <br />
      <Code content={content} copyable={true} />
    </React.Fragment>
  );
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
      <Definition title='Badges'>
        <Badge pkg={pkg} />
      </Definition>
      <Definition title='Commits range'>
        <DefinitionText content={
          `${versionData?.revs[0]} -> ${versionData?.revs[1]}`
        } />
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
