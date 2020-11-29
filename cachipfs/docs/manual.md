# Table of contents

<!-- http://ecotrust-canada.github.io/markdown-toc/ -->

- [Introduction](#introduction)
- [Installing](#installing)
- [Components](#components)
- [Using Nix-IPFS in your system](#using-nix-ipfs-in-your-system)

# Introduction

Nix-IPFS is a [binary cache](https://nixos.wiki/wiki/Binary_Cache) implementation over [IPFS](https://ipfs.io/).

A binary cache can store Nixpkgs, Nix builds, and in a more general sense /nix/store paths.

Results in the binary cache can be used by other machines to avoid building the result from source.
This helps you save the time, resources, and bandwidth required to build again.

Nix-IPFS serve those results over a peer-to-peer distributed file system,
enabling many powerful features:

- [Decentralization](https://en.wikipedia.org/wiki/Decentralization) of stored content.
- [Peer-to-peer](https://en.wikipedia.org/wiki/Peer-to-peer) content distribution.
- Cryptographic [content-addressing](https://en.wikipedia.org/wiki/Content-addressable_storage).

# Installing

You can install the latest release in your host system with:

`$ nix-env -i -f https://github.com/kamadorueda/nix-ipfs/archive/latest.tar.gz`

Alternatively if you clone the repository you can install from it:

`/my/repositories/nix-ipfs $ ./build/install.sh`

You can also use live commands without installing anything in your host:

`/my/repositories/nix-ipfs $ ./bin/<binary>`

# Components

The project is made up of three components:

- **Node**

  The component you need to execute in order to have an instance of Nix-IPFS working in your system.

  Binary: `$ nix-ipfs-node`

- **Coordinator**

  A micro-service exposing required functionality for the different nix-ipfs-node's to work.

  This is only for core developers of Nix-IPFS,
  a public running instance is running and ready to use (keep reading).

  Binary: `$ nix-ipfs-coordinator`

# Using Nix-IPFS in your system

Just install and run: `$ nix-ipfs-node`.

Some required environment variables configure the node.
We highly recommend you to add them permanently to your shell profile or something similar.

```bash
# Binary cache to follow
export NIX_IPFS_NODE_SUBSTITUTER='https://cache.nixos.org'

# Directory where to save data
export NIX_IPFS_NODE_DATA_DIR='~/.nix-ipfs'

# IPFS Daemon Ports
export NIX_IPFS_NODE_IPFS_API_PORT='8889'
export NIX_IPFS_NODE_IPFS_GATEWAY_PORT='8890'
export NIX_IPFS_NODE_IPFS_SWARM_PORT='8891'

# This node port
export NIX_IPFS_NODE_PORT='8888'

# Coordinator to connect to.
# This is pending to deploy, for now.
# Go back in a few days when I finish deploying the server:
#   https://github.com/kamadorueda/4shells.com
export NIX_IPFS_NODE_COORDINATOR_URL
```
