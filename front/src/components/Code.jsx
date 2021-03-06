// Third praty libraries
import dedentContent from 'dedent';
import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { defaultStyle as style } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { FileCopyOutlined } from '@material-ui/icons';
import { IconButton } from '@material-ui/core';
import { SplitDiv } from './SplitDiv';

const onCopy = () => alert('Copied!');

export const CopyButton = ({ content, type }) => {
  const style = { color: '#007bff' };

  return (
    <CopyToClipboard onCopy={onCopy} text={content}>
      <IconButton>
        <FileCopyOutlined fontSize='small'/>
      </IconButton>
    </CopyToClipboard>
  );
};

export const Highlight = ({
  content,
  lang,
}) => (
  <SyntaxHighlighter
    language={lang}
    style={style}
  >
    {content}
  </SyntaxHighlighter>
);

export const Code = ({
  content,
  dedent=true,
  copyable=false,
  lang,
}) => {
  const contentD = dedent ? dedentContent(content) : content;

  if (copyable) {
    return (
      <SplitDiv
        left={<CopyButton content={contentD} type='icon+copy' />}
        right={
          <Highlight
            content={contentD}
            lang={lang}
          />
        }
      />
    );
  }

  return (
    <Highlight
      content={contentD}
      lang={lang}
    />
  );
};

export const CodeBlock = ({ content, dedent, copyable, lang }) => {
  return (
    <React.Fragment>
      <hr />
      <Code content={content} copyable={copyable} dedent={dedent} lang={lang} />
      <hr />
    </React.Fragment>
  );
};
