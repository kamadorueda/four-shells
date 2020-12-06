// Third party libraries
import React from 'react';
import ReactMarkdown from 'react-markdown';
import gfm from 'remark-gfm';

// Local libraries
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
    <h2 id={id}>
      {renderLink({ children, href: `#${id}` })}
    </h2>
  );
};

const renderLink = ({ href, children }) => (
  <a href={href} target="_blank" rel='noreferrer noopener'>
    {children}
  </a>
);

const renderText = ({ children }) => (
  <span>
    {children}
  </span>
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

export const Markdown = ({ content }) => (
  <React.Fragment>
    <MarkDownBlock content={getTableOfContents(content)} />
    <MarkDownBlock content={content} />
  </React.Fragment>
);

export const renderMarkdown = ({ content }) => () => (
  <Markdown content={content} />
);
