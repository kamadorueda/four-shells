// Third party libraries
import React from 'react';

// Local
import { Index } from '../components/cachipfs/Index';
import { render } from '../utils/renderDOM';

// Side effects
render({
  generator: (props) => <Index {...props} />,
  title: "CachIPFS - Encrypted Nix Binary Cache over IPFS",
})
