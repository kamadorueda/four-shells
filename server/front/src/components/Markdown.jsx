// Third party libraries
import {
  Link,
} from '@material-ui/core';
import React from 'react';
import ReactMarkdown from 'react-markdown';
import gfm from 'remark-gfm';

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
    <h2 id={id}>
      <Link href={`#${id}`}>
        {children}
      </Link>
    </h2>
  );
};

const renderLink = ({ href, children }) => (
  <Link href={href}>
    {children}
  </Link>
);

const renderText = ({ children }) => (
  <span>
    {children}
  </span>
);

const getAnchorId = (text) => text.toLowerCase().replaceAll(' ', '-');

const getTableOfContents = (content) => {
  const lines = content
    .split('\n')
    .filter((line) => line.startsWith('#'))
    .map((line) => line.split(' '))
    .map((components) => ({
      level: components.slice(0, 1).join(' ').length,
      title: components.slice(1).join(' '),
    }));

  if (lines.length > 0) {
    let toc = [];
    toc.push('# Table of contents');
    toc.push();
    for (const { level, title } of lines) {
      toc.push(`- ${' '.repeat(level)} [${title}](#${getAnchorId(title)})`);
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

export const Markdown = ({ content, title }) => (
  <React.Fragment>
    <MarkDownBlock content={`# ${title}`} />
    <MarkDownBlock content={getTableOfContents(content)} />
    <MarkDownBlock content={content} />
  </React.Fragment>
);

export const renderMarkdown = ({ content, title }) => () => (
  <Markdown content={content} title={title} />
);
