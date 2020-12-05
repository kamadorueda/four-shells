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

const renderHeading = ({ children, level }) => (
  React.createElement(
    "h".concat(level + 1), {}, children,
  )
);

const renderLink = ({ href, children}) => (
  <Link href={href}>
    {children}
  </Link>
);

const renderText = ({ children }) => (
  <span>
    {children}
  </span>
);

export const Markdown = ({ content }) => (
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
)
