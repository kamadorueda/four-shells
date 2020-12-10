// Third party libraries
import { Divider, Link, Typography } from '@material-ui/core';
import React from 'react';
import ReactMarkdown from 'react-markdown';
import gfm from 'remark-gfm';

// Local libraries
import { THEME } from '../utils/theme';
import { CodeBlock } from './Code';

const renderBreak = () => (
  <br />
);

const renderCode = ({ language, value }) => (
  <CodeBlock
    content={value}
    dedent={false}
    lang={language}
  />
);

const renderHeading = ({ children, level }) => {
  const id = getAnchorId(children[0].props.children);

  return (
    <Typography component='h2' id={id}>
      {renderLink({ children, href: `#${id}` })}
    </Typography>
  );
};

const renderLink = ({ href, children }) => (
  <Link href={href} style={{ color: THEME.own.link }}>
    <b>{children}</b>
  </Link>
);

const renderText = ({ children }) => (
  <Typography component='span'>
    {children}
  </Typography>
);

const getAnchorId = (text) => text.toLowerCase().replaceAll(' ', '-');

const getTableOfContents = (content) => {
  let inBlock = false;
  let titles = []
  for (let line of content.split('\n')) {
    if (line.startsWith('#') && !inBlock) {
      titles.push(line);
    } else if (line.startsWith('```')) {
      inBlock = !inBlock;
    }
  }

  titles = titles
    .map((line) => line.split(' '))
    .map((components) => ({
      level: components.slice(0, 1).join(' ').length,
      title: components.slice(1).join(' '),
    }));

  if (titles.length > 0) {
    let toc = [];
    toc.push('# Table of contents');
    toc.push();
    for (const { level, title } of titles) {
      toc.push(`${'   '.repeat(level)}1. [${title}](#${getAnchorId(title)})`);
    }

    return toc.join('\n');
  }

  return '';
}

const MarkDownBlock = ({ content }) => (
  <ReactMarkdown
    children={content}
    plugins={[gfm]}
    renderers={{
      break: renderBreak,
      code: renderCode,
      heading: renderHeading,
      link: renderLink,
      text: renderText,
    }}
  />
);

export const Markdown = ({ content }) => (
  <React.Fragment>
    <MarkDownBlock content={getTableOfContents(content)} />
    <br />
    <Divider />
    <br />
    <br />
    <MarkDownBlock content={content} />
  </React.Fragment>
);

export const renderMarkdown = (content) => () => (
  <Markdown content={content} />
);
