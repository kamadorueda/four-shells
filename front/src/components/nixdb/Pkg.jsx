// Third party libraries
import {
  Card,
  CardContent,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  Link,
  MenuItem,
  RadioGroup,
  Select,
  TextField,
  Typography,
} from '@material-ui/core';
import {
  ArrowForwardOutlined,
  MemoryOutlined,
  PersonOutlineOutlined,
  RadioButtonUncheckedOutlined,
} from '@material-ui/icons';
import React, { useEffect, useState } from 'react';
import { Redirect, useParams } from 'react-router-dom';
import compareVersions from 'compare-versions';

// Local libraries
import { THEME } from '../../utils/theme';
import { Code } from '../Code';
import { Progress } from '../Progress';
import { SplitDiv } from '../SplitDiv';
import { DATA_URL, useFetchJSON } from './utils';

// Constants
const COLORS = [
  'blue',
  'blueviolet',
  'brightgreen',
  'green',
  'lightgrey',
  'orange',
  'red',
  'yellow',
  'yellowgreen',
];

const STYLES = [
  'flat',
  'flat-square',
  'plastic',
  'for-the-badge',
];

const FORMATS_FUNCTIONS = {
  'AsciiDoc': (imageURL, linkURL) => `
    image:${imageURL}[link='${linkURL}']
  `,
  'HTML': (imageURL, linkURL) => `
    <a href='${linkURL}'>
      <img src='${imageURL}'>
    </a>
  `,
  'Markdown': (imageURL, linkURL) => `
    [![](${imageURL})](${linkURL})
  `,
  'ReStructuredText': (imageURL, linkURL) => `
    .. image:: ${imageURL}
      :target: ${linkURL}
  `,
};

const FORMATS = Object.keys(FORMATS_FUNCTIONS);

const badge = ({
  color = 'green',
  label,
  labelColor = 'grey',
  logo = 'NixOS',
  logoColor = 'white',
  pkg,
  style = 'flat',
}) => {
  const url = new URL('https://img.shields.io/endpoint');

  url.searchParams.set('color', color);
  url.searchParams.set('label', label === undefined ? pkg : label);
  url.searchParams.set('labelColor', labelColor);
  url.searchParams.set('logo', logo);
  url.searchParams.set('logoColor', logoColor);
  url.searchParams.set('style', style);
  url.searchParams.set('url', `${DATA_URL}/badges/${pkg}.json`);

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

const DefinitionText = ({ icon, content }) => (
  <Typography component='span' color='textSecondary' gutterBottom variant='body2'>
    {icon ? (
      <IconButton size='small'>
        {icon}
      </IconButton>
    ) : undefined}
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
      case 'string':
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
  const [content, setContent] = useState('');
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

  const onBadgeSelection = (content, radioID) => () => {
    setContent(content);
    setBadgeId(radioID);
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
      <br />
      <FormControl variant='outlined'>
        <InputLabel>Format</InputLabel>
        <Select
          value={format}
          onChange={onChangeFormat}
          label='Format'
        >
          {FORMATS.map((f) => <MenuItem key={f} value={f}>{f}</MenuItem>)}
        </Select>
        <br />
        <TextField
          defaultValue={pkg}
          label='Custom label'
          onChange={onChangeLabel}
          value={label}
          variant='outlined'
        />
      </FormControl>
      <br />
      <br />
      <Grid container spacing={0}>
        <RadioGroup row>
          {badgesData.map(({ badgeContent, color, imageURL, style }) => {
            const radioID = `${style}/${color}`;

            return (
              <Grid item xs={12} sm={6} md={4} lg={4} xl={4}>
                <SplitDiv
                  left={
                    <IconButton
                      onClick={onBadgeSelection(badgeContent, radioID)}
                      size='small'
                    >
                      {radioID === badgeId
                        ? <ArrowForwardOutlined />
                        : <RadioButtonUncheckedOutlined />}
                    </IconButton>
                  }
                  right={<img alt={radioID} src={imageURL}/>}
                />
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

const getVersionsFromPkgData = (data) => {
  let versions = data.map(([version, _]) => version);

  try {
    versions = versions.sort(compareVersions).reverse();
  } catch {
    // Version(s) are not valid semver so fall back to original data sort.
    // (Unfortunately a number of libraries do not quite use fully "correct" semantic versioning).
    // Default sort is alphabetical, basically
    versions = versions.reverse();
  }

  return versions;
}

export const Pkg = () => {
  const { pkg, version } = useParams();

  const dataJSON = useFetchJSON(`/pkgs/${pkg}.json`, {});
  const data =  Object.entries(dataJSON);

  // While data is an empty list we should show a progress to the user
  if (data.length === 0) {
    return <Progress />
  }

  // At this point the user may have accessed a package but no version
  // Let's sort versions semantically
  const versions = getVersionsFromPkgData(data);

  // If there is no version let's redirect to the latest version
  if (version === undefined) {
    return <Redirect to={`/pkg/${encodeURIComponent(pkg)}/${encodeURIComponent(versions[0])}`} />;
  }

  // We have now a version, let's display its associated data
  const versionData = dataJSON[version];
  const versionDataLastRev = versionData?.revs[1];
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
        <Grid container spacing={0}>
          {versions.map((v) => (
            <Grid key={v} item xs={6} sm={6} md={4} lg={4} xl={3}>
              <DefinitionText
                content={
                  <Link
                    href={`/nixdb/pkg/${encodeURIComponent(pkg)}/${encodeURIComponent(v)}`}
                    style={{ color: THEME.own.link}}
                  >
                    {v}
                  </Link>
                }
              />
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
        <Grid container spacing={0}>
          {formatMaintainers(versionData?.meta?.maintainers).map((m) => (
            <Grid key={m} item xs={6} sm={6} md={4} lg={4} xl={3}>
              <DefinitionText
                icon={<PersonOutlineOutlined/>}
                content={m}
              />
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
        <Grid container spacing={0}>
          {formatPlatforms(versionData?.meta?.platforms).map((p) => (
            <Grid key={p} item xs={6} sm={6} md={4} lg={4} xl={3}>
              <DefinitionText
                icon={<MemoryOutlined/>}
                content={p}
              />
            </Grid>
          ))}
        </Grid>
      </Definition>
    </Card>
  );
}
