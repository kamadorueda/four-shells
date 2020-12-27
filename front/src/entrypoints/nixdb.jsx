// Third party libraries
import React from 'react';

// Local
import { Index } from '../components/nixdb/Index';
import { render } from '../utils/renderDOM';

// Side effects
render({
  generator: (props) => <Index {...props} />,
  title: "NixDB - Nix packages database",
})
